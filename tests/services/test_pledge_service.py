import copy
import unittest
from unittest.mock import Mock

import pytest

from my_app.api.domain import PledgePrototype
from my_app.api.exceptions import CancellationException
from my_app.api.services import PledgeService
from tests.utils.mock_data import MOCK_PLEDGE, MOCK_CAMPAIGN

mock_pledge_repository = Mock()
pledge_service = PledgeService(mock_pledge_repository)


class TestPledgeService(unittest.TestCase):

    def setUp(self):
        mock_pledge_repository.reset_mock()

    def test_create_pledge_returns_created_pledge(self):
        mock_pledge_repository.create_pledge.return_value = MOCK_PLEDGE

        created_pledge = pledge_service.create_pledge(
            PledgePrototype(
                buyer_id=1,
                pledge_price=34,
                campaign_id=1
            )
        )

        assert created_pledge.id == MOCK_PLEDGE.id
        mock_pledge_repository.create_pledge.assert_called_once()

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
