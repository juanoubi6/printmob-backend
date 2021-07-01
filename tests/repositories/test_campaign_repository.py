import unittest
from typing import List
from unittest.mock import MagicMock, patch

import pytest

from my_app.api.domain import Campaign, Page, CampaignModelImage, Buyer
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import CampaignRepository
from tests.utils.mock_data import MOCK_CAMPAIGN_MODEL, MOCK_FILTERS, MOCK_CAMPAIGN_MODEL_IMAGE_PROTOTYPE, \
    MOCK_CAMPAIGN_MODEL_IMAGE_MODEL, MOCK_ORDER_MODEL
from tests.utils.test_data import TEST_CAMPAIGN_PROTOTYPE

test_db = MagicMock()
campaign_repository = CampaignRepository(test_db)


class TestCampaignRepository(unittest.TestCase):

    def setUp(self):
        test_db.reset_mock()

    def test_create_campaign_creates_campaign(self):
        response = campaign_repository.create_campaign(TEST_CAMPAIGN_PROTOTYPE)

        assert isinstance(response, Campaign)

        test_db.session.add.assert_called()
        test_db.session.flush.assert_called_once()
        test_db.session.commit.assert_called_once()

    def test_get_campaign_detail_returns_campaign(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.return_value = MOCK_CAMPAIGN_MODEL

        response = campaign_repository.get_campaign_detail(1)

        assert isinstance(response, Campaign)
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.assert_called_once()

    def test_get_campaign_detail_throws_error_when_campaign_is_not_found(self):
        test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            campaign_repository.get_campaign_detail(1)

    @patch('my_app.api.repositories.campaign_repository.paginate')
    def test_get_campaigns_returns_campaign_page(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_CAMPAIGN_MODEL]

        response = campaign_repository.get_campaigns(MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

    def test_create_campaign_model_image_creates_campaign_model_image(self):
        response = campaign_repository.create_campaign_model_image(MOCK_CAMPAIGN_MODEL_IMAGE_PROTOTYPE)

        assert isinstance(response, CampaignModelImage)

        test_db.session.add.assert_called_once()
        test_db.session.commit.assert_called_once()

    def test_delete_campaign_model_image_returns_campaign_model_image_on_success(self):
        test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_CAMPAIGN_MODEL_IMAGE_MODEL

        response = campaign_repository.delete_campaign_model_image(1)

        assert isinstance(response, CampaignModelImage)
        test_db.session.query.return_value.filter_by.return_value.first.assert_called_once()
        test_db.session.delete.assert_called_once_with(MOCK_CAMPAIGN_MODEL_IMAGE_MODEL)
        test_db.session.commit.assert_called_once()

    def test_delete_campaign_model_image_throws_error_when_campaign_model_image_is_not_found(self):
        test_db.session.query.return_value.filter_by.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            campaign_repository.delete_campaign_model_image(1)

    @patch('my_app.api.repositories.campaign_repository.paginate')
    def test_get_campaign_orders_returns_order_page(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_ORDER_MODEL]

        response = campaign_repository.get_campaign_orders(1, MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()
