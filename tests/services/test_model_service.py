import copy
import unittest
from unittest.mock import Mock, patch, MagicMock

import pytest

from my_app.api.domain import Page
from my_app.api.exceptions import BusinessException
from my_app.api.services import ModelService
from tests.test_utils.mock_entities import MOCK_RAW_IMAGE_FILE, MOCK_MODEL, MOCK_MODEL_PROTOTYPE, MOCK_MODEL_IMAGE, \
    MOCK_MODEL_LIKE, MOCK_MODEL_CATEGORY, MOCK_MODEL_PURCHASE


class TestModelService(unittest.TestCase):

    def setUp(self):
        self.mock_model_repository = Mock()
        self.mock_s3_repository = Mock()
        self.mock_executor = Mock()
        self.mock_email_repository = Mock()
        self.model_service = ModelService(
            self.mock_model_repository, self.mock_s3_repository, self.mock_executor, self.mock_email_repository
        )

    def test_create_model_creates_model_with_file(self):
        self.mock_s3_repository.upload_file.return_value = "url"
        self.mock_model_repository.create_model.return_value = MOCK_MODEL

        created_model = self.model_service.create_model(MOCK_MODEL_PROTOTYPE, MOCK_RAW_IMAGE_FILE, [MOCK_RAW_IMAGE_FILE])

        assert created_model == MOCK_MODEL
        self.mock_model_repository.create_model.assert_called_once()

    def test_create_model_raises_error_if_allow_purchases_is_true_but_no_purchase_price_was_provided(self):
        invalid_model_prototype = copy.deepcopy(MOCK_MODEL_PROTOTYPE)
        invalid_model_prototype.allow_purchases = True
        invalid_model_prototype.purchase_price = None

        with pytest.raises(BusinessException):
            self.model_service.create_model(invalid_model_prototype, MOCK_RAW_IMAGE_FILE, [MOCK_RAW_IMAGE_FILE])

    def test_create_model_raises_error_if_allow_alliance_is_true_but_no_desired_percentage_was_provided(self):
        invalid_model_prototype = copy.deepcopy(MOCK_MODEL_PROTOTYPE)
        invalid_model_prototype.allow_alliances = True
        invalid_model_prototype.desired_percentage = None

        with pytest.raises(BusinessException):
            self.model_service.create_model(invalid_model_prototype, MOCK_RAW_IMAGE_FILE, [MOCK_RAW_IMAGE_FILE])

    def test_create_model_raises_error_if_allow_alliance_is_true_and_desired_percentage_is_bigger_than_50(self):
        invalid_model_prototype = copy.deepcopy(MOCK_MODEL_PROTOTYPE)
        invalid_model_prototype.allow_alliances = True
        invalid_model_prototype.desired_percentage = 50.1

        with pytest.raises(BusinessException):
            self.model_service.create_model(invalid_model_prototype, MOCK_RAW_IMAGE_FILE, [MOCK_RAW_IMAGE_FILE])

    @patch('my_app.api.services.model_service.uuid')
    def test_create_model_image_returns_model_image_on_success(self, uuid_mock):
        self.mock_s3_repository.upload_file.return_value = "image_url"
        self.mock_model_repository.create_model_image.return_value = MOCK_MODEL_IMAGE
        uuid_mock.uuid4.return_value = "uuid4_value"

        model_image = self.model_service.create_model_image(1, MOCK_RAW_IMAGE_FILE)
        expected_image_path = "model_images/uuid4_value"

        assert model_image == MOCK_MODEL_IMAGE
        self.mock_s3_repository.upload_file.assert_called_once_with(MOCK_RAW_IMAGE_FILE, expected_image_path)
        self.mock_model_repository.create_model_image.assert_called_once()

        called_prototype = self.mock_model_repository.create_model_image.call_args[0][0]
        assert called_prototype.model_id == 1
        assert called_prototype.file_name == expected_image_path
        assert called_prototype.model_picture_url == "image_url"

    def test_delete_model_image_deletes_image(self):
        self.mock_model_repository.delete_model_image.return_value = MOCK_MODEL_IMAGE

        self.model_service.delete_model_image(MOCK_MODEL_IMAGE.id)

        self.mock_model_repository.delete_model_image.assert_called_once_with(1)
        self.mock_s3_repository.delete_file.assert_called_once_with(MOCK_MODEL_IMAGE.file_name)

    def test_get_model_categories_returns_model_categories(self):
        self.mock_model_repository.get_model_categories.return_value = [MOCK_MODEL_CATEGORY]

        response = self.model_service.get_model_categories()

        assert response == [MOCK_MODEL_CATEGORY]
        self.mock_model_repository.get_model_categories.assert_called_once()

    def test_add_like_to_model_returns_model_like(self):
        self.mock_model_repository.add_like_to_model.return_value = MOCK_MODEL_LIKE

        response = self.model_service.add_like_to_model(1, 2)

        assert response == MOCK_MODEL_LIKE
        self.mock_model_repository.add_like_to_model.assert_called_once_with(1, 2)

    def test_remove_like_from_model_success(self):
        self.model_service.remove_like_from_model(1, 2)

        self.mock_model_repository.remove_like_from_model.assert_called_once_with(1, 2)

    def test_create_model_purchase_sends_email_to_designer_and_returns_model_purchase(self):
        self.mock_model_repository.create_model_purchase.return_value = MOCK_MODEL_PURCHASE

        response = self.model_service.create_model_purchase(1, 2, 3)

        assert response == MOCK_MODEL_PURCHASE
        self.mock_model_repository.create_model_purchase.assert_called_once_with(1, 2, 3)
        self.mock_executor.submit.assert_called_once()

    def test_get_printer_model_purchases_returns_model_purchases_page(self):
        self.mock_model_repository.get_printer_model_purchases.return_value = Page(1, 2, 3, [MOCK_MODEL_PURCHASE])

        filters = {"filter": "filter"}
        created_page = self.model_service.get_printer_model_purchases(1, filters)

        assert created_page.page == 1
        self.mock_model_repository.get_printer_model_purchases.assert_called_once_with(1, filters)

    def test_get_model_detail_returns_model(self):
        self.mock_model_repository.get_model_detail.return_value = MOCK_MODEL

        result = self.model_service.get_model_detail(1, 2)

        assert result == MOCK_MODEL
        self.mock_model_repository.get_model_detail.assert_called_once_with(1, 2)

    def test_get_models_returns_model_page(self):
        self.mock_model_repository.get_models.return_value = Page(1, 2, 3, [MOCK_MODEL])

        filters = {"filter": "filter"}
        created_page = self.model_service.get_models(filters, 1)

        assert created_page.page == 1
        self.mock_model_repository.get_models.assert_called_once_with(filters, 1)

    def test_get_model_ordering_returns_model_ordering(self):
        response = self.model_service.get_model_ordering()

        assert len(response) == 2
        assert response[0].name == "MOST_LIKED"
        assert response[0].value == "Más populares"
        assert response[1].name == "MOST_RECENT"
        assert response[1].value == "Más recientes"

    def test_get_designer_models_returns_model_page(self):
        self.mock_model_repository.get_designer_models.return_value = Page(1, 2, 3, [MOCK_MODEL])

        filters = {"filter": "filter"}
        created_page = self.model_service.get_designer_models(1, filters)

        assert created_page.page == 1
        self.mock_model_repository.get_designer_models.assert_called_once_with(1, filters)

    def test_delete_model_success(self):
        self.model_service.delete_model(1, 2)

        self.mock_model_repository.delete_model.assert_called_once_with(1, 2)

    def test_get_model_purchase_from_printer_returns_model_purchase(self):
        self.mock_model_repository.get_model_purchase_from_printer.return_value = MOCK_MODEL_PURCHASE

        result = self.model_service.get_model_purchase_from_printer(1, 2)

        assert result == MOCK_MODEL_PURCHASE
        self.mock_model_repository.get_model_purchase_from_printer.assert_called_once_with(1, 2)
