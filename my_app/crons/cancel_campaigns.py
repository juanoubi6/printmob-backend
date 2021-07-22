import datetime
import logging
from concurrent.futures import Executor

from sqlalchemy.orm import sessionmaker, noload

from my_app.api.domain import CampaignStatus
from my_app.api.repositories import EmailRepository
from my_app.api.repositories.models import CampaignModel, FailedToRefundPledgeModel
from my_app.api.utils.email import create_cancelled_campaign_email_for_client


def cancel_campaigns(
        session_factory: sessionmaker,
        email_repository: EmailRepository,
        executor: Executor,
        mercadopago_repository
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

                            # TODO Get mercadopago payment id of printer's transaction, refund it and create a refund transaction
                            """ 
                            mp_printer_payment_id_to_refund = pledge_to_cancel.printer_transaction.mp_payment_id

                            mercadopagoRepository.refund_transactions(mp_printer_payment_id_to_refund)

                            session.add(
                                TransactionModel(
                                    mp_payment_id=pledge_to_cancel.printer_transaction.mp_payment_id,
                                    user_id=pledge_to_cancel.printer_transaction.user_id,
                                    amount=pledge_to_cancel.printer_transaction.amount,
                                    type=TransactionStatus.REFUND,
                                    is_future=False
                                )
                            )
                            """

                            # TODO Get mercadopago payment id of desginer's transaction, refund it and create a refund transaction
                            #  (may not be necessary)
                            """
                            if pledge_to_cancel.designer_transaction is not None:
                                mp_designer_payment_id_to_refund = pledge_to_cancel.designer_transaction.mp_payment_id

                                mercadopagoRepository.refund_transactions(mp_designer_payment_id_to_refund)

                                session.add(
                                    TransactionModel(
                                        mp_payment_id=pledge_to_cancel.designer_transaction.mp_payment_id,
                                        user_id=pledge_to_cancel.designer_transaction.user_id,
                                        amount=pledge_to_cancel.designer_transaction.amount,
                                        type=TransactionStatus.REFUND,
                                        is_future=False
                                    )
                                )
                            """

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