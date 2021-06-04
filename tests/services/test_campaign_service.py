from unittest.mock import Mock

from my_app.api.domain import Page
from my_app.api.services import CampaignService
from tests.mock_data import MOCK_CAMPAIGN

mock_campaign_repository = Mock()
campaign_service = CampaignService(mock_campaign_repository)


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
