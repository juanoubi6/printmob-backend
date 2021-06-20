import datetime
import logging
from concurrent.futures import Executor

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, noload

from my_app.api.domain import CampaignStatus
from my_app.api.repositories import EmailRepository
from my_app.api.repositories.models import CampaignModel
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
                .filter(CampaignModel.deleted_at == None) \
                .filter(CampaignModel.status == CampaignStatus.IN_PROGRESS.value) \
                .filter(func.date(CampaignModel.end_date) <= datetime.date.today()) \
                .options(noload(CampaignModel.tech_detail)) \
                .options(noload(CampaignModel.images)) \
                .all()

            emails_to_send = []
            mercadopago_payment_ids_to_refund = []
            refund_transactions = []

            for campaign_to_finish in campaigns_to_finish:
                if len(campaign_to_finish.pledges) >= campaign_to_finish.min_pledgers:
                    # Change campaign status
                    campaign_to_finish.status = CampaignStatus.COMPLETED.value

                    # Create a complete campaign email to send to each pledger
                    emails_to_send.extend(
                        [
                            create_completed_campaign_email(pledge.buyer.user.email, campaign_to_finish)
                            for pledge in campaign_to_finish.pledges
                        ]
                    )
                else:
                    # Change campaign status
                    campaign_to_finish.status = CampaignStatus.UNSATISFIED.value

                    # For each pledge...
                    for pledge_to_cancel in campaign_to_finish.pledges:

                        # Create an unsatisfied campaign email to send to the buyer
                        emails_to_send.append(
                            create_unsatisfied_campaign_email(pledge_to_cancel.buyer.user.email, campaign_to_finish)
                        )

                        # Delete pledge
                        pledge_to_cancel.deleted_at = datetime.datetime.now()

                        # TODO Get mercadopago payment id of printer's transaction and create a refund transaction
                        """ 
                        mercadopago_payment_ids_to_refund.append(pledge_to_cancel.printer_transaction.mp_payment_id)
                        
                        refund_transactions.append(
                            TransactionModel(
                                mp_payment_id=pledge_to_cancel.printer_transaction.mp_payment_id,
                                user_id=pledge_to_cancel.printer_transaction.user_id,
                                amount=pledge_to_cancel.printer_transaction.amount,
                                type=TransactionStatus.REFUND,
                                is_future=False
                            )
                        )
                        """

                        # TODO Get mercadopago payment id of desginer's transaction and create a refund transaction
                        #  (may not be necessary)
                        """
                        if pledge_to_cancel.designer_transaction is not None:
                            mercadopago_payment_ids_to_refund.append(pledge_to_cancel.designer_transaction.mp_payment_id)
        
                            refund_transactions.append(
                                designer_refund_transaction = TransactionModel(
                                    mp_payment_id=pledge_to_cancel.designer_transaction.mp_payment_id,
                                    user_id=pledge_to_cancel.designer_transaction.user_id,
                                    amount=pledge_to_cancel.designer_transaction.amount,
                                    type=TransactionStatus.REFUND,
                                    is_future=False
                                )
                            )
                        """

            # TODO Refund transactions. If this fails..., TDB.
            """
            mercadopagoRepository.refund_transactions(mercadopago_payment_ids_to_refund)
            """

            # TODO Create refund transactions
            """
            session.add_all(refund_transactions)
            """

            session.commit()
        except Exception as exc:
            logging.error("Transaction error: {}".format(str(exc)))
            session.rollback()
            return

    # Send emails on background
    if len(emails_to_send) > 0:
        executor.submit(email_repository.send_many_emails, emails_to_send)

    return
