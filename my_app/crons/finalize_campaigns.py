import datetime
import logging
from concurrent.futures import Executor

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, noload

from my_app.api.domain import CampaignStatus, OrderStatus
from my_app.api.repositories import EmailRepository
from my_app.api.repositories.models import CampaignModel, FailedToRefundPledgeModel, OrderModel
from my_app.api.utils.email import create_completed_campaign_email_for_client, \
    create_unsatisfied_campaign_email_for_client, create_completed_campaign_email_for_printer, \
    create_unsatisfied_campaign_email_for_printer


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
                .filter(CampaignModel.status.in_([CampaignStatus.IN_PROGRESS.value, CampaignStatus.TO_BE_FINALIZED.value, CampaignStatus.CONFIRMED.value])) \
                .filter(func.date(CampaignModel.end_date) <= datetime.datetime.now()) \
                .options(noload(CampaignModel.tech_detail)) \
                .options(noload(CampaignModel.images)) \
                .all()

            client_completed_emails = []
            client_unsatisfied_emails = []
            printer_completed_emails = []
            printer_unsatisfied_emails = []
            failed_to_refund_pledges = []

            for campaign_to_finish in campaigns_to_finish:
                try:
                    if len(campaign_to_finish.pledges) >= campaign_to_finish.min_pledgers:
                        # Change campaign status to COMPLETED
                        campaign_to_finish.status = CampaignStatus.COMPLETED.value
                        campaign_to_finish.end_date = datetime.datetime.now()

                        # For each pledge...
                        for successful_pledge in campaign_to_finish.pledges:

                            # Create an order
                            session.add(
                                OrderModel(
                                    campaign_id=campaign_to_finish.id,
                                    pledge_id=successful_pledge.id,
                                    buyer_id=successful_pledge.buyer.id,
                                    status=OrderStatus.IN_PROGRESS.value
                                )
                            )

                        session.commit()

                        # Create a complete campaign email to send to each pledger
                        client_completed_emails.extend(
                            [
                                create_completed_campaign_email_for_client(pledge.buyer.user.email, campaign_to_finish)
                                for pledge in campaign_to_finish.pledges
                            ]
                        )

                        # Create a complete campaign email to send to the printer
                        printer_completed_emails.append(
                            create_completed_campaign_email_for_printer(
                                campaign_to_finish.printer.user.email, campaign_to_finish
                            )
                        )
                    else:
                        # Change campaign status to UNSATISFIED
                        campaign_to_finish.status = CampaignStatus.UNSATISFIED.value
                        session.commit()

                        # Create an unsatisfied campaign email to send to the printer
                        printer_unsatisfied_emails.append(
                            create_unsatisfied_campaign_email_for_printer(
                                campaign_to_finish.printer.user.email, campaign_to_finish
                            )
                        )

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

                                session.commit()

                                # Create an unsatisfied campaign email to send to the buyer
                                client_unsatisfied_emails.append(
                                    create_unsatisfied_campaign_email_for_client(pledge_to_cancel.buyer.user.email,
                                                                                 campaign_to_finish)
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
                        campaign_to_finish.id, str(exc)
                    ))
                    session.rollback()
        except Exception as exc:
            logging.error("Unhandled error on finalize campaign process: {}".format(str(exc)))
            session.rollback()

    # Save failed pledges
    if len(failed_to_refund_pledges) > 0:
        session.add_all(failed_to_refund_pledges)
        session.commit()

    # Send emails on background
    if len(client_completed_emails) > 0:
        executor.submit(email_repository.send_many_emails_of_the_same_type, client_completed_emails)
    if len(client_unsatisfied_emails) > 0:
        executor.submit(email_repository.send_many_emails_of_the_same_type, client_unsatisfied_emails)
    if len(printer_completed_emails) > 0:
        for email in printer_completed_emails:
            executor.submit(email_repository.send_individual_email, email)
    if len(printer_unsatisfied_emails) > 0:
        for email in printer_unsatisfied_emails:
            executor.submit(email_repository.send_individual_email, email)

    return
