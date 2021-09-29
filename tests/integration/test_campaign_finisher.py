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
        to_be_unsatisfied = self.created_campaigns['in_progress_wont_confirm_campaign']

        to_be_unsatisfied_campaign = self.session.query(CampaignModel).filter_by(id=to_be_unsatisfied['id']).first()
        unsatisfied_pledge_price = to_be_unsatisfied_campaign.pledge_price

        # check transaction sum of user before refund transaction
        result = self.session.execute(f"SELECT SUM(amount) FROM transactions WHERE user_id = {to_be_unsatisfied_campaign.printer_id}")
        amount_before_refund = result.fetchone()[0]

        self.cron_controller.finish_campaigns()

        # TEST CONFIRMED CAMPAIGN

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

        # TEST UNSATISFIED CAMPAIGN

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
