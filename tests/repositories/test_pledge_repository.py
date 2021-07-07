import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import PledgePrototype, Pledge, Campaign, CampaignStatus
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import PledgeRepository
from tests.test_utils.mock_models import MOCK_CAMPAIGN_MODEL, MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED, \
    MOCK_PLEDGE_MODEL

test_db = MagicMock()
test_mock_campaign_repository = MagicMock()
pledge_repository = PledgeRepository(test_db, test_mock_campaign_repository)


class TestPledgeRepository(unittest.TestCase):

    def setUp(self):
        test_db.reset_mock()
        test_mock_campaign_repository.reset_mock()

    def test_create_pledge_returns_created_pledge(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_CAMPAIGN_MODEL
        ]

        test_proto = PledgePrototype(
            buyer_id=1,
            campaign_id=1,
            pledge_price=34
        )

        response = pledge_repository.create_pledge(test_proto, False)

        assert isinstance(response, Pledge)
        test_db.session.add.assert_called_once()
        test_db.session.commit.assert_called_once()

    def test_create_pledge_change_campaign_status_and_returns_created_pledge(self):
        campaign_model = MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED
        test_mock_campaign_repository.get_campaign_detail.return_value = campaign_model

        test_proto = PledgePrototype(
            buyer_id=1,
            campaign_id=1,
            pledge_price=34
        )

        response = pledge_repository.create_pledge(test_proto, True)

        assert campaign_model.status == CampaignStatus.TO_BE_FINALIZED.value
        assert isinstance(response, Pledge)
        test_db.session.add.assert_called_once()
        test_db.session.commit.assert_called_once()

    def test_get_pledge_campaigns_returns_campaign_when_found(self):
        # Because the way the pledge and the campaign are looked up on DB are the same, we use a side effect
        # mock with a different return value on each call.
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL, MOCK_CAMPAIGN_MODEL
        ]

        response = pledge_repository.get_pledge_campaign(1)

        assert isinstance(response, Campaign)
        assert test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 2

    def test_get_pledge_campaigns_raises_exception_when_pledge_cannot_be_found(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            None, MOCK_CAMPAIGN_MODEL
        ]

        with pytest.raises(NotFoundException):
            pledge_repository.get_pledge_campaign(1)

        assert test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 1

    def test_get_pledge_campaigns_raises_exception_when_campaign_cannot_be_found(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL, None
        ]

        with pytest.raises(NotFoundException):
            pledge_repository.get_pledge_campaign(1)

        assert test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 2

    def test_get_pledge_returns_pledge_when_found(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL]

        response = pledge_repository.get_pledge(1)

        assert isinstance(response, Pledge)
        assert test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 1

    def test_get_pledge_raises_exception_when_pledge_cannot_be_found(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [None]

        with pytest.raises(NotFoundException):
            pledge_repository.get_pledge(1)

    def test_delete_pledge_returns_deleted_pledge_on_success(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [
            MOCK_PLEDGE_MODEL
        ]

        response = pledge_repository.delete_pledge(1)

        assert isinstance(response, Pledge)
        assert response.deleted_at is not None
        assert test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.call_count == 1
        test_db.session.commit.assert_called_once()

    def test_delete_pledge_raises_exception_when_pledge_cannot_be_found(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.side_effect = [None]

        with pytest.raises(NotFoundException):
            pledge_repository.delete_pledge(1)

    def test_get_pledges_returns_pledge_list(self):
        # The 2 filter mocks correspond to the deleted_at filter and campaign_id filter
        test_db.session.query.return_value.filter.return_value.filter.return_value.options.return_value.order_by.return_value.all.return_value = [
            MOCK_PLEDGE_MODEL
        ]

        response = pledge_repository.get_pledges({"campaign_id": 1})

        assert len(response) == 1
        assert isinstance(response[0], Pledge)

    def test_has_pledge_in_campaign_returns_true_when_pledge_exists(self):
        test_db.session\
            .query.return_value\
            .filter.return_value\
            .filter.return_value\
            .filter.return_value\
            .options.return_value\
            .first.return_value = MOCK_PLEDGE_MODEL

        response = pledge_repository.has_pledge_in_campaign(buyer_id=1, campaign_id=1)

        assert response is True
