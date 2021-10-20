import datetime
import logging
from concurrent.futures import Executor

from sqlalchemy.orm import sessionmaker, noload

from my_app.api.domain import CampaignStatus, TransactionType
from my_app.api.repositories import EmailRepository, MercadopagoRepository
from my_app.api.repositories.models import CampaignModel, FailedToRefundPledgeModel, TransactionModel
from my_app.api.utils.email import create_cancelled_campaign_email_for_client


def cancel_campaigns(
        session_factory: sessionmaker,
        email_repository: EmailRepository,
        executor: Executor,
        mercadopago_repository: MercadopagoRepository
):
    logging.info("Starting cancel campaigns process")

    with session_factory() as session:
        try:
            campaigns_to_cancel = session.query(CampaignModel) \
                .filter(CampaignModel.deleted_at == None) \
                .filter(CampaignModel.status == CampaignStatus.TO_BE_CANCELLED.value) \
                .options(noload(CampaignModel.tech_detail)) \
                .options(noload(CampaignModel.images)) \
                .all()

            campaign_cancellation_emails = []
            failed_to_refund_pledges = []

            for campaign_to_cancel in campaigns_to_cancel:
                try:
                    # Change campaign status to COMPLETED
                    campaign_to_cancel.status = CampaignStatus.CANCELLED.value
                    session.commit()

                    # For each pledge...
                    for pledge_to_cancel in campaign_to_cancel.pledges:
                        try:
                            # Delete pledge
                            pledge_to_cancel.deleted_at = datetime.datetime.now()

                            # Refund mercadopago printer transaction payment and create a refund transaction
                            mercadopago_repository.refund_payment(
                                pledge_to_cancel.printer_transaction.mp_payment_id
                            )

                            session.add(
                                TransactionModel(
                                    mp_payment_id=pledge_to_cancel.printer_transaction.mp_payment_id,
                                    user_id=pledge_to_cancel.printer_transaction.user_id,
                                    amount=pledge_to_cancel.printer_transaction.amount*-1,
                                    type=TransactionType.REFUND.value,
                                    is_future=pledge_to_cancel.printer_transaction.is_future
                                )
                            )

                            # Create a refund designer transaction (if necessary)
                            if pledge_to_cancel.designer_transaction is not None:
                                session.add(
                                    TransactionModel(
                                        mp_payment_id=pledge_to_cancel.designer_transaction.mp_payment_id,
                                        user_id=pledge_to_cancel.designer_transaction.user_id,
                                        amount=pledge_to_cancel.designer_transaction.amount * -1,
                                        type=TransactionType.REFUND.value,
                                        is_future=pledge_to_cancel.designer_transaction.is_future
                                    )
                                )

                            session.commit()

                            # Create an campaign cancellation email to send to the buyer
                            campaign_cancellation_emails.append(
                                create_cancelled_campaign_email_for_client(
                                    pledge_to_cancel.buyer.user.email, campaign_to_cancel
                                )
                            )

                        except Exception as exc:
                            session.rollback()
                            error = str(exc)
                            logging.error("Pledge {} could not be refunded. Err: {}".format(pledge_to_cancel.id, error))
                            failed_to_refund_pledges.append(FailedToRefundPledgeModel(
                                pledge_id=pledge_to_cancel.id,
                                fail_date=datetime.datetime.now(),
                                error=error
                            ))

                except Exception as exc:
                    logging.error("Error when updating campaign of id {}. Error: {}".format(
                        campaign_to_cancel.id, str(exc)
                    ))
                    session.rollback()
        except Exception as exc:
            logging.error("Unhandled error on cancel campaign process: {}".format(str(exc)))
            return

    # Save failed pledges
    if len(failed_to_refund_pledges) > 0:
        session.add_all(failed_to_refund_pledges)
        session.commit()

    # Send emails on background
    if len(campaign_cancellation_emails) > 0:
        executor.submit(email_repository.send_many_emails_of_the_same_type, campaign_cancellation_emails)

    return
