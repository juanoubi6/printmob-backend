import unittest
from unittest.mock import Mock, patch

import pytest

from my_app.api.domain import Page
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException
from my_app.api.services import CampaignService
from tests.test_utils.mock_entities import MOCK_CAMPAIGN, MOCK_CAMPAIGN_MODEL_IMAGE, MOCK_FILE, MOCK_ORDER, \
    MOCK_CAMPAIGN_PROTOTYPE

mock_campaign_repository = Mock()
mock_printer_repository = Mock()
mock_s3_repository = Mock()
campaign_service = CampaignService(mock_campaign_repository, mock_printer_repository, mock_s3_repository)


class TestCampaignService(unittest.TestCase):

    def setUp(self):
        mock_campaign_repository.reset_mock()
        mock_printer_repository.reset_mock()
        mock_s3_repository.reset_mock()

    def test_create_campaigns_creates_a_campaign(self):
        mock_printer_repository.exists_printer.return_value = True
        mock_campaign_repository.create_campaign.return_value = MOCK_CAMPAIGN

        created_campaign = campaign_service.create_campaign(MOCK_CAMPAIGN_PROTOTYPE)

        assert created_campaign == MOCK_CAMPAIGN
        mock_printer_repository.exists_printer.assert_called_once_with(MOCK_CAMPAIGN_PROTOTYPE.printer_id)
        mock_campaign_repository.create_campaign.assert_called_once_with(MOCK_CAMPAIGN_PROTOTYPE)

    def test_does_not_create_campaign_if_printer_does_not_exists(self):
        mock_printer_repository.exists_printer.return_value = False

        with pytest.raises(UnprocessableEntityException):
            campaign_service.create_campaign(MOCK_CAMPAIGN_PROTOTYPE)
            mock_printer_repository.exists_printer.assert_called_once_with(MOCK_CAMPAIGN_PROTOTYPE.printer_id)
            mock_campaign_repository.create_campaign.assert_not_called()

    def test_get_campaigns_returns_campaigns_page(self):
        mock_campaign_repository.get_campaigns.return_value = Page(1, 2, 3, [MOCK_CAMPAIGN])

        filters = {"filter": "filter"}
        created_page = campaign_service.get_campaigns(filters)

        assert created_page.page == 1
        mock_campaign_repository.get_campaigns.assert_called_once_with(filters)

    def test_get_campaign_detail_returns_campaigns(self):
        mock_campaign_repository.get_campaign_detail.return_value = MOCK_CAMPAIGN

        campaign = campaign_service.get_campaign_detail(1)

        assert campaign == MOCK_CAMPAIGN
        mock_campaign_repository.get_campaign_detail.assert_called_once_with(1)

    @patch('my_app.api.services.campaign_service.uuid')
    def test_create_campaign_model_image_returns_campaign_model_image_on_success(self, uuid_mock):
        mock_s3_repository.upload_file.return_value = "image_url"
        mock_campaign_repository.create_campaign_model_image.return_value = MOCK_CAMPAIGN_MODEL_IMAGE
        uuid_mock.uuid4.return_value = "uuid4_value"

        campaign_model_image = campaign_service.create_campaign_model_image(1, MOCK_FILE)
        expected_image_path = "campaign_model_images/uuid4_value"

        assert campaign_model_image == MOCK_CAMPAIGN_MODEL_IMAGE
        mock_s3_repository.upload_file.assert_called_once_with(MOCK_FILE, expected_image_path)
        mock_campaign_repository.create_campaign_model_image.assert_called_once()

        called_prototype = mock_campaign_repository.create_campaign_model_image.call_args[0][0]
        assert called_prototype.campaign_id == 1
        assert called_prototype.file_name == expected_image_path
        assert called_prototype.model_picture_url == "image_url"

    def test_delete_campaign_model_image_deletes_image(self):
        mock_campaign_repository.delete_campaign_model_image.return_value = MOCK_CAMPAIGN_MODEL_IMAGE

        campaign_service.delete_campaign_model_image(MOCK_CAMPAIGN_MODEL_IMAGE.id)

        mock_campaign_repository.delete_campaign_model_image.assert_called_once_with(1)
        mock_s3_repository.delete_file.assert_called_once_with(MOCK_CAMPAIGN_MODEL_IMAGE.file_name)

    def test_get_campaign_orders_returns_order_page(self):
        mock_campaign_repository.get_campaign_orders.return_value = Page(1, 2, 3, [MOCK_ORDER])

        filters = {"filter": "filter"}
        orders_page = campaign_service.get_campaign_orders(1, filters)

        assert orders_page.page == 1
        mock_campaign_repository.get_campaign_orders.assert_called_once_with(1,filters)

    def test_get_buyer_campaigns_returns_campaigns_page(self):
        mock_campaign_repository.get_buyer_campaigns.return_value = Page(1, 2, 3, [MOCK_CAMPAIGN])

        filters = {"filter": "filter"}
        created_page = campaign_service.get_buyer_campaigns(1, filters)

        assert created_page.page == 1
        mock_campaign_repository.get_buyer_campaigns.assert_called_once_with(1, filters)