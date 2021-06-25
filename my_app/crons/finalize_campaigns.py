import datetime
import logging
from concurrent.futures import Executor

from sqlalchemy import func, and_, or_
from sqlalchemy.orm import sessionmaker, noload

from my_app.api.domain import CampaignStatus
from my_app.api.repositories import EmailRepository
from my_app.api.repositories.models import CampaignModel, FailedToRefundPledgeModel
from my_app.api.utils.email import create_completed_campaign_email, create_unsatisfied_campaign_email


def finalize_campaign(
        session_factory: sessionmaker,
        email_repository: EmailRepository,
        executor: Executor,
        mercadopago_repository
):
    logging.info("Starting finishing campaigns process")

    with session_factory() as session:
        try:
            campaigns_to_finish = session.query(CampaignModel) \
                .filter(
                and_(CampaignModel.deleted_at == None,
                     or_(CampaignModel.status == CampaignStatus.TO_BE_FINALIZED,
                         and_(
                             CampaignModel.status == CampaignStatus.IN_PROGRESS.value,
                             func.date(CampaignModel.end_date) <= datetime.date.today()
                         ))
                     )
                ) \
                .options(noload(CampaignModel.tech_detail)) \
                .options(noload(CampaignModel.images)) \
                .all()

            emails_to_send = []
            failed_to_refund_pledges = []

            for campaign_to_finish in campaigns_to_finish:
                if len(campaign_to_finish.pledges) >= campaign_to_finish.min_pledgers:
                    try:
                        # Change campaign status to COMPLETED
                        campaign_to_finish.status = CampaignStatus.COMPLETED.value
                        session.commit()

                        # Create a complete campaign email to send to each pledger
                        emails_to_send.extend(
                            [
                                create_completed_campaign_email(pledge.buyer.user.email, campaign_to_finish)
                                for pledge in campaign_to_finish.pledges
                            ]
                        )
                    except Exception as exc:
                        logging.error("Successful campaign of id {} could not be updated. Error: {}".format(
                            campaign_to_finish.id, str(exc)
                        ))
                        session.rollback()
                else:
                    # Change campaign status to UNSATISFIED
                    campaign_to_finish.status = CampaignStatus.UNSATISFIED.value
                    session.commit()

                    # For each pledge...
                    for pledge_to_cancel in campaign_to_finish.pledges:
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

                            # Create an unsatisfied campaign email to send to the buyer
                            emails_to_send.append(
                                create_unsatisfied_campaign_email(pledge_to_cancel.buyer.user.email, campaign_to_finish)
                            )

                            session.commit()
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
            session.rollback()
            logging.error("Unhandled error on finalize campaign process: {}".format(str(exc)))
            return

    # Save failed pledges
    if len(failed_to_refund_pledges) > 0:
        session.add_all(failed_to_refund_pledges)
        session.commit()

    # Send emails on background
    if len(emails_to_send) > 0:
        executor.submit(email_repository.send_many_emails, emails_to_send)

    return
