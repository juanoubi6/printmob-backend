import datetime
import logging
from concurrent.futures import Executor

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, noload

from my_app.api.domain import CampaignStatus, OrderStatus, TransactionType
from my_app.api.repositories import EmailRepository, MercadopagoRepository
from my_app.api.repositories.models import CampaignModel, FailedToRefundPledgeModel, OrderModel, TransactionModel, \
    ModelModel
from my_app.api.utils.email import create_completed_campaign_email_for_client, \
    create_unsatisfied_campaign_email_for_client, create_completed_campaign_email_for_printer, \
    create_unsatisfied_campaign_email_for_printer, create_completed_campaign_email_with_model_file_url_for_printer


def finalize_campaign(
        session_factory: sessionmaker,
        email_repository: EmailRepository,
        executor: Executor,
        mercadopago_repository: MercadopagoRepository
):
    logging.info("Starting finishing campaigns process")

    with session_factory() as session:
        try:
            campaigns_to_finish_by_end_date = session.query(CampaignModel) \
                .filter(CampaignModel.deleted_at == None) \
                .filter(CampaignModel.status.in_([CampaignStatus.IN_PROGRESS.value, CampaignStatus.CONFIRMED.value])) \
                .filter(func.date(CampaignModel.end_date) <= datetime.datetime.now()) \
                .options(noload(CampaignModel.tech_detail)) \
                .options(noload(CampaignModel.images)) \
                .all()

            campaigns_to_finish_by_max_pledge_goal = session.query(CampaignModel) \
                .filter(CampaignModel.deleted_at == None) \
                .filter(CampaignModel.status == CampaignStatus.TO_BE_FINALIZED.value) \
                .options(noload(CampaignModel.tech_detail)) \
                .options(noload(CampaignModel.images)) \
                .all()

            campaigns_to_finish = campaigns_to_finish_by_end_date + campaigns_to_finish_by_max_pledge_goal

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

                        # If the campaign has an associated model, get the file URL
                        file_url = None
                        if campaign_to_finish.model_id is not None:
                            model_model = session.query(ModelModel).filter(
                                ModelModel.id == campaign_to_finish.model_id
                            ).first()
                            file_url = model_model.model_file.model_file_url

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

                            # Update transaction's if_future value (from True to False)
                            successful_pledge.printer_transaction.is_future = False
                            if successful_pledge.designer_transaction is not None:
                                successful_pledge.designer_transaction.is_future = False

                        session.commit()

                        # Create a complete campaign email to send to each pledger
                        client_completed_emails.extend(
                            [
                                create_completed_campaign_email_for_client(pledge.buyer.user.email, campaign_to_finish)
                                for pledge in campaign_to_finish.pledges
                            ]
                        )

                        # Create a complete campaign email to send to the printer
                        if file_url is None:
                            printer_completed_emails.append(
                                create_completed_campaign_email_for_printer(
                                    campaign_to_finish.printer.user.email, campaign_to_finish
                                )
                            )
                        else:
                            printer_completed_emails.append(
                                create_completed_campaign_email_with_model_file_url_for_printer(
                                    campaign_to_finish.printer.user.email, campaign_to_finish, file_url
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
