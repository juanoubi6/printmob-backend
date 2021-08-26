import datetime
import unittest
from unittest.mock import MagicMock, patch

import pytest

from my_app.api.domain import Campaign, Page, CampaignModelImage, CampaignStatus
from my_app.api.exceptions import NotFoundException, MercadopagoException, CampaignCreationException
from my_app.api.repositories import CampaignRepository
from my_app.api.repositories.models import CampaignModel
from tests.test_utils.mock_entities import MOCK_FILTERS, MOCK_CAMPAIGN_MODEL_IMAGE_PROTOTYPE, MOCK_CAMPAIGN_PROTOTYPE
from tests.test_utils.mock_models import MOCK_CAMPAIGN_MODEL, MOCK_CAMPAIGN_MODEL_IMAGE_MODEL, MOCK_ORDER_MODEL


class TestCampaignRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = MagicMock()
        self.mock_mercadopago_repository = MagicMock()
        self.campaign_repository = CampaignRepository(self.test_db, self.mock_mercadopago_repository)

    def test_create_campaign_creates_campaign(self):
        self.mock_mercadopago_repository.create_campaign_pledge_preference.return_value = "some_preference_id"
        response = self.campaign_repository.create_campaign(MOCK_CAMPAIGN_PROTOTYPE)

        assert isinstance(response, Campaign)
        assert response.mp_preference_id == "some_preference_id"

        self.test_db.session.add.assert_called()
        self.test_db.session.flush.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_create_campaign_rollbacks_and_raises_mercadopago_exception_on_mercadopago_error(self):
        self.mock_mercadopago_repository.create_campaign_pledge_preference.side_effect = MercadopagoException(
            "Some error")

        with pytest.raises(MercadopagoException):
            self.campaign_repository.create_campaign(MOCK_CAMPAIGN_PROTOTYPE)

        self.test_db.session.rollback.assert_called_once()

    def test_create_campaign_rollbacks_and_raises_campaign_creation_exception_on_database_error(self):
        self.mock_mercadopago_repository.create_campaign_pledge_preference.return_value = "some_preference_id"
        self.test_db.session.commit.side_effect = Exception("Some db error")

        with pytest.raises(CampaignCreationException):
            self.campaign_repository.create_campaign(MOCK_CAMPAIGN_PROTOTYPE)

        self.test_db.session.rollback.assert_called_once()

    def test_get_campaign_detail_returns_campaign(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.return_value = MOCK_CAMPAIGN_MODEL

        response = self.campaign_repository.get_campaign_detail(1)

        assert isinstance(response, Campaign)
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.assert_called_once()

    def test_get_campaign_detail_throws_error_when_campaign_is_not_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            self.campaign_repository.get_campaign_detail(1)

    @patch('my_app.api.repositories.campaign_repository.paginate')
    def test_get_campaigns_returns_campaign_page(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_CAMPAIGN_MODEL]

        response = self.campaign_repository.get_campaigns(MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

    def test_create_campaign_model_image_creates_campaign_model_image(self):
        response = self.campaign_repository.create_campaign_model_image(MOCK_CAMPAIGN_MODEL_IMAGE_PROTOTYPE)

        assert isinstance(response, CampaignModelImage)

        self.test_db.session.add.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_delete_campaign_model_image_returns_campaign_model_image_on_success(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_CAMPAIGN_MODEL_IMAGE_MODEL

        response = self.campaign_repository.delete_campaign_model_image(1)

        assert isinstance(response, CampaignModelImage)
        self.test_db.session.query.return_value.filter_by.return_value.first.assert_called_once()
        self.test_db.session.delete.assert_called_once_with(MOCK_CAMPAIGN_MODEL_IMAGE_MODEL)
        self.test_db.session.commit.assert_called_once()

    def test_delete_campaign_model_image_throws_error_when_campaign_model_image_is_not_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            self.campaign_repository.delete_campaign_model_image(1)

    @patch('my_app.api.repositories.campaign_repository.paginate')
    def test_get_campaign_orders_returns_order_page(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_ORDER_MODEL]

        response = self.campaign_repository.get_campaign_orders(1, MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

    @patch('my_app.api.repositories.campaign_repository.paginate')
    def test_get_buyer_campaigns_returns_campaign_page(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_CAMPAIGN_MODEL]

        response = self.campaign_repository.get_buyer_campaigns(1, MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

    def test_change_campaign_status_changes_campaign(self):
        campaign_to_change = CampaignModel(
            id=1,
            name="Campaign name",
            description="Description",
            campaign_picture_url="campaign picture url",
            pledge_price=10.50,
            end_date=datetime.datetime(2020, 5, 17),
            min_pledgers=5,
            max_pledgers=10,
            tech_detail=None,
            images=[],
            printer=None,
            pledges=[],
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17),
            status="In progress"
        )

        self.test_db.session.query.return_value.filter_by.return_value.filter.return_value.first.return_value = campaign_to_change

        self.campaign_repository.change_campaign_status(1, CampaignStatus.TO_BE_CANCELLED)

        self.test_db.session.commit.assert_called_once()
        assert campaign_to_change.status == CampaignStatus.TO_BE_CANCELLED.value
