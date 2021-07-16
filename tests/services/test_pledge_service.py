import copy
import datetime
import unittest
from unittest.mock import Mock

import pytest

from my_app.api.domain import PledgePrototype
from my_app.api.exceptions import CancellationException
from my_app.api.exceptions.pledge_creation_exception import PledgeCreationException
from my_app.api.services import PledgeService
from tests.test_utils.mock_entities import MOCK_PLEDGE, MOCK_CAMPAIGN

mock_pledge_repository = Mock()
mock_campaign_repository = Mock()
pledge_service = PledgeService(mock_pledge_repository, mock_campaign_repository)


class TestPledgeService(unittest.TestCase):

    def setUp(self):
        mock_pledge_repository.reset_mock()
        mock_campaign_repository.reset_mock()

    def test_create_pledge_returns_created_pledge_when_campaign_is_not_completed_and_campaign_has_max_pledgers_value(self):
        uncompleted_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        uncompleted_campaign.min_pledgers = 100
        uncompleted_campaign.max_pledgers = 150
        uncompleted_campaign.current_pledgers = 50

        mock_campaign_repository.get_campaign_detail.return_value = uncompleted_campaign
        mock_pledge_repository.has_pledge_in_campaign.return_value = False
        mock_pledge_repository.create_pledge.return_value = MOCK_PLEDGE

        created_pledge = pledge_service.create_pledge(
            PledgePrototype(
                buyer_id=1,
                campaign_id=1,
                pledge_price=34
            )
        )

        assert created_pledge.id == MOCK_PLEDGE.id
        mock_pledge_repository.create_pledge.assert_called_once()

    def test_create_pledge_returns_created_pledge_when_campaign_is_not_completed_and_campaign_has_no_max_pledgers_value(self):
        uncompleted_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        uncompleted_campaign.min_pledgers = 100
        uncompleted_campaign.max_pledgers = None
        uncompleted_campaign.current_pledgers = 50

        mock_campaign_repository.get_campaign_detail.return_value = uncompleted_campaign
        mock_pledge_repository.has_pledge_in_campaign.return_value = False
        mock_pledge_repository.create_pledge.return_value = MOCK_PLEDGE

        created_pledge = pledge_service.create_pledge(
            PledgePrototype(
                buyer_id=1,
                campaign_id=1,
                pledge_price=34
            )
        )

        assert created_pledge.id == MOCK_PLEDGE.id
        mock_pledge_repository.create_pledge.assert_called_once()

    def test_create_pledge_raises_error_when_buyer_has_an_existing_pledge_in_the_campaign(self):
        uncompleted_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        uncompleted_campaign.min_pledgers = 100
        uncompleted_campaign.max_pledgers = None
        uncompleted_campaign.current_pledgers = 50

        mock_campaign_repository.get_campaign_detail.return_value = uncompleted_campaign
        mock_pledge_repository.has_pledge_in_campaign.return_value = True
        mock_pledge_repository.create_pledge.return_value = MOCK_PLEDGE

        with pytest.raises(PledgeCreationException):
            pledge_service.create_pledge(
                PledgePrototype(
                    buyer_id=1,
                    campaign_id=1,
                    pledge_price=34
                )
            )

    def test_create_pledge_throws_exception_if_campaign_has_reached_max_pledgers(self):
        completed_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        completed_campaign.min_pledgers = 100
        completed_campaign.max_pledgers = 120
        completed_campaign.current_pledgers = 120

        mock_campaign_repository.get_campaign_detail.return_value = completed_campaign

        with pytest.raises(PledgeCreationException):
            pledge_service.create_pledge(
                PledgePrototype(
                    buyer_id=1,
                    campaign_id=1,
                    pledge_price=34
                )
            )

    def test_create_pledge_raises_error_when_campaign_end_date_was_already_reached(self):
        finished_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        finished_campaign.end_date = datetime.datetime(2019, 5, 17)

        mock_campaign_repository.get_campaign_detail.return_value = finished_campaign

        with pytest.raises(PledgeCreationException):
            pledge_service.create_pledge(
                PledgePrototype(
                    buyer_id=1,
                    campaign_id=1,
                    pledge_price=34
                )
            )

    def test_cancel_pledge_executes_successfully_when_its_campaign_has_not_reached_its_goal(self):
        uncompleted_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        uncompleted_campaign.min_pledgers = 100
        uncompleted_campaign.current_pledgers = 50

        mock_pledge_repository.get_pledge_campaign.return_value = uncompleted_campaign

        pledge_service.cancel_pledge(1)

        mock_pledge_repository.get_pledge_campaign.assert_called_once()
        mock_pledge_repository.delete_pledge.assert_called_once_with(1)

    def test_cancel_pledge_raises_exception_when_its_campaign_has_reached_its_goal(self):
        completed_campaign = copy.deepcopy(MOCK_CAMPAIGN)
        completed_campaign.min_pledgers = 100
        completed_campaign.current_pledgers = 120

        mock_pledge_repository.get_pledge_campaign.return_value = completed_campaign

        with pytest.raises(CancellationException):
            pledge_service.cancel_pledge(1)

        mock_pledge_repository.get_pledge_campaign.assert_called_once()
        mock_pledge_repository.delete_pledge.assert_not_called()

    def test_get_pledges_return_pledge_list(self):
        mock_pledge_repository.get_pledges.return_value = [MOCK_PLEDGE]

        pledges = pledge_service.get_pledges({"campaign_id": 1})

        assert pledges == [MOCK_PLEDGE]
        mock_pledge_repository.get_pledges.assert_called_once_with({"campaign_id": 1})
