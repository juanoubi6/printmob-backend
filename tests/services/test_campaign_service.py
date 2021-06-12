from unittest.mock import Mock

import pytest
from tests.utils.mock_data import MOCK_CAMPAIGN
from tests.utils.test_data import TEST_CAMPAIGN_PROTOTYPE

from my_app.api.domain import Page
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException
from my_app.api.services import CampaignService

mock_campaign_repository = Mock()
mock_printer_repository = Mock()
campaign_service = CampaignService(mock_campaign_repository, mock_printer_repository)


def test_create_campaigns_creates_a_campaign():
    mock_printer_repository.exists_printer.return_value = True
    mock_campaign_repository.create_campaign.return_value = MOCK_CAMPAIGN

    created_campaign = campaign_service.create_campaign(TEST_CAMPAIGN_PROTOTYPE)

    assert created_campaign == MOCK_CAMPAIGN
    mock_printer_repository.exists_printer.assert_called_once_with(TEST_CAMPAIGN_PROTOTYPE.printer_id)
    mock_campaign_repository.create_campaign.assert_called_once_with(TEST_CAMPAIGN_PROTOTYPE)


def test_does_not_create_campaign_if_printer_does_not_exists():
    mock_printer_repository.exists_printer.return_value = False

    with pytest.raises(UnprocessableEntityException):
        campaign_service.create_campaign(TEST_CAMPAIGN_PROTOTYPE)
        mock_printer_repository.exists_printer.assert_called_once_with(TEST_CAMPAIGN_PROTOTYPE.printer_id)
        mock_campaign_repository.create_campaign.assert_not_called()


def test_get_campaigns_returns_campaigns_page():
    mock_campaign_repository.get_campaigns.return_value = Page(1, 2, 3, [MOCK_CAMPAIGN])

    filters = {"filter": "filter"}
    created_page = campaign_service.get_campaigns(filters)

    assert created_page.page == 1
    mock_campaign_repository.get_campaigns.assert_called_once_with(filters)


def test_get_campaign_detail_returns_campaigns():
    mock_campaign_repository.get_campaign_detail.return_value = MOCK_CAMPAIGN

    campaign = campaign_service.get_campaign_detail(1)

    assert campaign == MOCK_CAMPAIGN
    mock_campaign_repository.get_campaign_detail.assert_called_once_with(1)
