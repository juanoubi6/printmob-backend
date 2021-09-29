import os

import unittest
from unittest.mock import Mock

from my_app.api.domain import CampaignStatus
from my_app.api.builder import build_mercadopago_sdk
from my_app.api.db_builder import create_db_session_factory
from my_app.api.controllers.cron_controller import CronController
from my_app.api.repositories import MercadopagoRepository
from my_app.api.repositories.models import CampaignModel


class TestIntegrationCancelCampaigns(unittest.TestCase):

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

    def test_cancel_campaigns(self):

        to_be_cancelled_camp = self.created_campaigns['will_cancel']

        campaign = self.session.query(CampaignModel).filter_by(id=to_be_cancelled_camp['id']).first()
        result = self.session.execute(f"SELECT SUM(amount) FROM transactions WHERE type = 'Refund' AND user_id = {campaign.printer_id}")
        initial_refunds = result.fetchone()[0]
        total_pledge_amount = len(campaign.pledges) * campaign.pledge_price

        self.cron_controller.cancel_campaigns()

        # Refresh campaign with CANCELLED state
        self.session.refresh(campaign)
        pledges = campaign.pledges

        # Campaign's status now is CANCELLED
        assert campaign.status == CampaignStatus.CANCELLED.value, f"Campaign {campaign.id} is not CANCELLED"

        # All pledges were deleted
        for pledge in pledges:
            # The pledge was deleted
            assert pledge.deleted_at is not None, f"Pledge {pledge.id} was not deleted upon cancellation"

        result = self.session.execute(f"SELECT SUM(amount) FROM transactions WHERE type = 'Refund' AND user_id = {campaign.printer_id}")
        amount_after_refund = result.fetchone()[0]

        assert total_pledge_amount + abs(initial_refunds) == abs(amount_after_refund)

    def tearDown(self):
        self.session.close()
        self.cron_controller.truncate_tables()
