import datetime
import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import PledgePrototype, Pledge, Campaign, CampaignStatus
from my_app.api.exceptions import NotFoundException, MercadopagoException, BusinessException
from my_app.api.repositories import PledgeRepository
from tests.test_utils.mock_models import MOCK_CAMPAIGN_MODEL, MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED, \
    MOCK_PLEDGE_MODEL


class TestPledgeRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = MagicMock()
        self.mock_campaign_repository = MagicMock()
        self.mock_mercadopago_repository = MagicMock()
        self.pledge_repository = PledgeRepository(self.test_db, self.mock_campaign_repository,
                                                  self.mock_mercadopago_repository)

    def test_create_pledge_returns_created_pledge(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_CAMPAIGN_MODEL
        ]

        test_proto = PledgePrototype(
            buyer_id=1,
            campaign_id=1,
            pledge_price=34
        )

        response = self.pledge_repository.create_pledge(
            test_proto,
            confirm_campaign=False,
            finalize_campaign=False
        )

        assert isinstance(response, Pledge)
        self.test_db.session.add.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_create_pledge_change_campaign_status_and_end_date_when_finalize_campaign_flag_is_true_and_returns_created_pledge(self):
        campaign_model = MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED
        campaign_original_end_date = campaign_model.end_date
        self.mock_campaign_repository.get_campaign_model_by_id.return_value = campaign_model

        test_proto = PledgePrototype(
            buyer_id=1,
            campaign_id=1,
            pledge_price=34
        )

        response = self.pledge_repository.create_pledge(
            test_proto,
            confirm_campaign=False,
            finalize_campaign=True
        )

        assert campaign_model.status == CampaignStatus.TO_BE_FINALIZED.value
        assert campaign_model.end_date <= campaign_original_end_date
        assert campaign_model.end_date.day <= (
                    datetime.datetime.now() + datetime.timedelta(days=1)).day  # Assert the end date is tomorrow date
        assert isinstance(response, Pledge)
        self.test_db.session.add.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_create_pledge_change_campaign_status_when_confirm_campaign_flag_is_true_and_returns_created_pledge(self):
        campaign_model = MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED
        campaign_original_end_date = campaign_model.end_date
        self.mock_campaign_repository.get_campaign_model_by_id.return_value = campaign_model

        test_proto = PledgePrototype(
            buyer_id=1,
            campaign_id=1,
            pledge_price=34
        )

        response = self.pledge_repository.create_pledge(
            test_proto,
            confirm_campaign=True,
            finalize_campaign=False
        )

        assert campaign_model.status == CampaignStatus.CONFIRMED.value
        assert campaign_model.end_date == campaign_original_end_date
        assert isinstance(response, Pledge)
        self.test_db.session.add.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_get_pledge_campaigns_returns_campaign_when_found(self):
        # Because the way the pledge and the campaign are looked up on DB are the same, we use a side effect
        # mock with a different return value on each call.
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL, MOCK_CAMPAIGN_MODEL
        ]

        response = self.pledge_repository.get_pledge_campaign(1)

        assert isinstance(response, Campaign)
        assert self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 2

    def test_get_pledge_campaigns_raises_exception_when_pledge_cannot_be_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            None, MOCK_CAMPAIGN_MODEL
        ]

        with pytest.raises(NotFoundException):
            self.pledge_repository.get_pledge_campaign(1)

        assert self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 1

    def test_get_pledge_campaigns_raises_exception_when_campaign_cannot_be_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL, None
        ]

        with pytest.raises(NotFoundException):
            self.pledge_repository.get_pledge_campaign(1)

        assert self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 2

    def test_get_pledge_returns_pledge_when_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL]

        response = self.pledge_repository.get_pledge(1)

        assert isinstance(response, Pledge)
        assert self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 1

    def test_get_pledge_raises_exception_when_pledge_cannot_be_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [None]

        with pytest.raises(NotFoundException):
            self.pledge_repository.get_pledge(1)

    def test_delete_pledge_returns_deleted_pledge_on_success(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL
        ]

        response = self.pledge_repository.delete_pledge(1)

        assert isinstance(response, Pledge)
        assert response.deleted_at is not None
        assert self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 1
        self.test_db.session.commit.assert_called_once()
        self.mock_mercadopago_repository.refund_payment.assert_called_once_with(
            MOCK_PLEDGE_MODEL.printer_transaction.mp_payment_id
        )

    def test_delete_pledge_rollbacks_entity_creations_on_refund_failure(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL
        ]
        self.mock_mercadopago_repository.refund_payment.side_effect = MercadopagoException("Some refund error")

        with pytest.raises(BusinessException):
            self.pledge_repository.delete_pledge(1)

        self.test_db.session.commit.assert_not_called()
        self.test_db.session.rollback.assert_called_once()

    def test_delete_pledge_raises_exception_when_pledge_cannot_be_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [None]

        with pytest.raises(NotFoundException):
            self.pledge_repository.delete_pledge(1)

    def test_get_pledges_returns_pledge_list(self):
        # The 2 filter mocks correspond to the deleted_at filter and campaign_id filter
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.options.return_value.order_by.return_value.all.return_value = [
            MOCK_PLEDGE_MODEL
        ]

        response = self.pledge_repository.get_pledges({"campaign_id": 1})

        assert len(response) == 1
        assert isinstance(response[0], Pledge)

    def test_has_pledge_in_campaign_returns_true_when_pledge_exists(self):
        self.test_db.session \
            .query.return_value \
            .filter.return_value \
            .filter.return_value \
            .filter.return_value \
            .options.return_value \
            .first.return_value = MOCK_PLEDGE_MODEL

        response = self.pledge_repository.has_pledge_in_campaign(buyer_id=1, campaign_id=1)

        assert response is True
