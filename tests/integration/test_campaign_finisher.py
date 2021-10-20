import datetime
import os

import unittest
from unittest.mock import Mock

from my_app.api.domain import CampaignStatus
from my_app.api.builder import build_mercadopago_sdk
from my_app.api.db_builder import create_db_session_factory
from my_app.api.controllers.cron_controller import CronController
from my_app.api.repositories import MercadopagoRepository
from my_app.api.repositories.models import CampaignModel, OrderModel, TransactionModel


class TestIntegrationFinishCampaigns(unittest.TestCase):

    def setUp(self):
        db_session_factory = create_db_session_factory(os.environ["DATABASE_URL"])
        executor = Mock()
        email_repository_mock = Mock()
        mercadopago_repository = MercadopagoRepository(
            build_mercadopago_sdk(),
            os.environ["PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS"],
            os.environ["PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT"],
            os.environ["PREFERENCE_BACK_URL_FOR_SUCCESS_MODEL_PURCHASE_PAYMENT"],
            os.environ["PREFERENCE_BACK_URL_FOR_MODEL_PURCHASE_ERRORS"]
        )

        self.cron_controller = CronController(db_session_factory, email_repository_mock, executor, mercadopago_repository)
        request_args = Mock()
        request_args.args = {'truncate': True}

        response = self.cron_controller.create_test_data(request_args)
        body = response[0]
        self.created_campaigns = body['created_campaigns']
        self.session = db_session_factory()

    def test_finish_campaigns(self):

        to_be_finished = self.created_campaigns['will_finish']
        to_be_unsatisfied = self.created_campaigns['in_progress_wont_confirm']
        with_alliance = self.created_campaigns['confirmed_with_model']

        to_be_unsatisfied_campaign = self.session.query(CampaignModel).filter_by(id=to_be_unsatisfied['id']).first()
        unsatisfied_pledge_price = to_be_unsatisfied_campaign.pledge_price

        # check transaction sum of user before refund transaction
        result = self.session.execute(f"SELECT SUM(amount) FROM transactions WHERE user_id = {to_be_unsatisfied_campaign.printer_id}")
        amount_before_refund = result.fetchone()[0]

        # Modify to_be_unsatisfied_campaign so it gets finished (changing it's end date)
        to_be_unsatisfied_campaign.end_date = datetime.datetime.now() - datetime.timedelta(days=1)
        self.session.commit()

        # Finish campaigns
        self.cron_controller.finish_campaigns()

        ################# TEST CONFIRMED CAMPAIGN #################

        confirmed_campaign = self.session.query(CampaignModel).filter_by(id=to_be_finished['id']).first()
        pledges = confirmed_campaign.pledges

        # Campaign's status is now COMPLETED
        assert confirmed_campaign.status == CampaignStatus.COMPLETED.value, f"Campaign {confirmed_campaign.id} is not COMPLETED"

        # For every pledge, a new order is created
        for pledge in pledges:
            # The pledge created an order
            assert self.session.query(OrderModel).filter_by(pledge_id=pledge.id).count() == 1

            # The transaction is not future now
            transaction = self.session.query(TransactionModel).filter_by(id=pledge.printer_transaction_id).first()
            assert transaction.is_future is False

        ################# TEST CONFIRMED CAMPAIGN WITH MODEL ALLIANCE #################

        with_alliance_campaign = self.session.query(CampaignModel).filter_by(id=with_alliance['id']).first()
        model = with_alliance_campaign.model
        desired_percentage = model.desired_percentage
        pledges = with_alliance_campaign.pledges

        pledges_earned_sum = 0
        designer_earned_sum = 0
        printer_earned_sum = 0
        for pledge in pledges:
            pledges_earned_sum += pledge.pledge_price

            designer_transaction = self.session.query(TransactionModel).filter_by(id=pledge.designer_transaction_id).first()
            designer_earned_sum += designer_transaction.amount

            printer_transaction = self.session.query(TransactionModel).filter_by(id=pledge.printer_transaction_id).first()
            printer_earned_sum += printer_transaction.amount

        # Test for the sum of transactions for designer and printer are equal to the pledges transaction subtotal
        assert pledges_earned_sum == designer_earned_sum + printer_earned_sum, f"The sum of transactions for campaign {with_alliance_campaign.id} is not correct."

        # The percentage for each actor is correct
        assert designer_earned_sum == pledges_earned_sum * (desired_percentage / 100)
        assert printer_earned_sum == pledges_earned_sum * (1 - desired_percentage / 100)

        ################# TEST UNSATISFIED CAMPAIGN #################

        self.session.refresh(to_be_unsatisfied_campaign)
        pledges = to_be_unsatisfied_campaign.pledges

        assert to_be_unsatisfied_campaign.status == CampaignStatus.UNSATISFIED.value, f"Campaign {to_be_unsatisfied_campaign.id} is not UNSATISFIED"

        for pledge in pledges:
            # The pledge was deleted
            assert pledge.deleted_at is not None

        # check transaction sum of user after refund transaction
        result = self.session.execute(f"SELECT SUM(amount) FROM transactions WHERE user_id = {to_be_unsatisfied_campaign.printer_id}")
        amount_after_refund = result.fetchone()[0]

        assert amount_before_refund == amount_after_refund + unsatisfied_pledge_price

    def tearDown(self):
        self.session.close()
        self.cron_controller.truncate_tables()
