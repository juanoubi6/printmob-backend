import copy
import unittest
from unittest.mock import MagicMock, patch

import pytest

from my_app.api.domain import Model, ModelImage, ModelLike, Payment, ModelPurchase, Page
from my_app.api.exceptions import MercadopagoException, NotFoundException, BusinessException, ModelCreationException
from my_app.api.repositories import ModelRepository
from tests.test_utils.mock_entities import MOCK_MODEL_PROTOTYPE, MOCK_MODEL_FILE_PROTOTYPE, MOCK_MODEL_IMAGE_PROTOTYPE, \
    MOCK_FILTERS, MOCK_RAW_IMAGE_FILE, MOCK_RAW_MODEL_FILE
from tests.test_utils.mock_models import MOCK_MODEL_IMAGE_MODEL, MOCK_MODEL_LIKE_MODEL, MOCK_MODEL_CATEGORY_MODEL, \
    MOCK_MODEL_MODEL, MOCK_MODEL_PURCHASE_MODEL


class TestModelRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = MagicMock()
        self.mock_mercadopago_repository = MagicMock()
        self.mock_s3_repository = MagicMock()
        self.model_repository = ModelRepository(self.test_db, self.mock_mercadopago_repository, self.mock_s3_repository)

    def test_create_model_creates_model_and_mercadopago_preference_if_model_allows_purchases(self):
        self.mock_mercadopago_repository.create_model_purchase_preference.return_value = "some_preference_id"
        self.mock_s3_repository.upload_file.return_value = "url_from_s3"
        response = self.model_repository.create_model(
            MOCK_MODEL_PROTOTYPE,
            MOCK_RAW_MODEL_FILE,
            [MOCK_RAW_IMAGE_FILE, MOCK_RAW_IMAGE_FILE]
        )

        assert isinstance(response, Model)
        assert (response.mp_preference_id, "some_preference_id")
        self.mock_mercadopago_repository.create_model_purchase_preference.assert_called_once()
        assert self.mock_s3_repository.upload_file.call_count == 3  # 1 model file, 2 images
        assert self.test_db.session.add.call_count == 2
        assert self.test_db.session.flush.call_count == 2
        self.test_db.session.commit.assert_called_once()

    def test_create_model_creates_model_without_mercadopago_preference_if_model_does_not_allow_purchases(self):
        model_that_does_not_allow_purchases = copy.deepcopy(MOCK_MODEL_PROTOTYPE)
        model_that_does_not_allow_purchases.allow_purchases = False

        response = self.model_repository.create_model(
            model_that_does_not_allow_purchases, MOCK_RAW_MODEL_FILE, [MOCK_RAW_IMAGE_FILE]
        )

        assert isinstance(response, Model)
        assert (response.mp_preference_id, None)
        self.mock_mercadopago_repository.create_model_purchase_preference.assert_not_called()
        assert self.test_db.session.add.call_count == 2
        assert self.test_db.session.flush.call_count == 2
        self.test_db.session.commit.assert_called_once()

    def test_create_model_creates_model_rollbacks_on_mercadopago_error(self):
        self.mock_mercadopago_repository.create_model_purchase_preference.side_effect = MercadopagoException("error")

        with pytest.raises(MercadopagoException):
            self.model_repository.create_model(MOCK_MODEL_PROTOTYPE, MOCK_RAW_MODEL_FILE, [MOCK_RAW_IMAGE_FILE])

        self.test_db.session.rollback.assert_called_once()

    def test_create_model_creates_model_rollbacks_on_commit_error_and_deletes_created_images_in_s3_if_present(self):
        self.mock_mercadopago_repository.create_model_purchase_preference.return_value = "some_preference_id"
        self.mock_s3_repository.upload_file.return_value = "url_from_s3"
        self.test_db.session.commit.side_effect = Exception("Some error")

        with pytest.raises(ModelCreationException):
            self.model_repository.create_model(MOCK_MODEL_PROTOTYPE, MOCK_RAW_MODEL_FILE, [MOCK_RAW_IMAGE_FILE])

        self.test_db.session.rollback.assert_called_once()
        assert self.mock_s3_repository.delete_file.call_count == 2  # Delete model file and image

    def test_create_model_image_creates_model_image(self):
        response = self.model_repository.create_model_image(MOCK_MODEL_IMAGE_PROTOTYPE)

        assert isinstance(response, ModelImage)

        self.test_db.session.add.assert_called_once()
        self.test_db.session.commit.assert_called_once()

    def test_delete_model_image_returns_model_image_on_success(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_MODEL_IMAGE_MODEL

        response = self.model_repository.delete_model_image(1)

        assert isinstance(response, ModelImage)
        self.test_db.session.query.return_value.filter_by.return_value.first.assert_called_once()
        self.test_db.session.delete.assert_called_once_with(MOCK_MODEL_IMAGE_MODEL)
        self.test_db.session.commit.assert_called_once()

    def test_delete_model_image_throws_error_when_model_image_is_not_found(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            self.model_repository.delete_model_image(1)

    def test_get_model_categories_returns_category_list(self):
        self.test_db.session.query.return_value.all.return_value = [MOCK_MODEL_CATEGORY_MODEL]

        response = self.model_repository.get_model_categories()

        assert len(response) == 1
        assert response[0].id == MOCK_MODEL_CATEGORY_MODEL.id

    def test_add_like_to_model_creates_model_like_if_it_does_not_exist(self):
        # First call returns the model, the second one returns the model like
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.side_effect = [
            MOCK_MODEL_MODEL, None
        ]

        response = self.model_repository.add_like_to_model(1, 2)

        assert isinstance(response, ModelLike)
        self.test_db.session.commit.assert_called_once()

    def test_add_like_to_model_returns_existing_model_like_if_it_does_exist(self):
        # First call returns the model, the second one returns the model like
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.side_effect = [
            MOCK_MODEL_MODEL, MOCK_MODEL_LIKE_MODEL
        ]

        response = self.model_repository.add_like_to_model(1, 2)

        assert isinstance(response, ModelLike)
        self.test_db.session.commit.assert_not_called()

    def test_remove_like_from_model_success(self):
        # First call returns the model, the second one returns the model like
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.side_effect = [
            MOCK_MODEL_MODEL, MOCK_MODEL_LIKE_MODEL
        ]

        self.model_repository.remove_like_from_model(1, MOCK_MODEL_LIKE_MODEL.user_id)

        self.test_db.session.commit.assert_called_once()

    def test_remove_like_from_model_raises_exception_if_the_user_removing_the_like_is_not_the_like_owner(self):
        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_MODEL_LIKE_MODEL

        with pytest.raises(BusinessException):
            self.model_repository.remove_like_from_model(1, 99)

    def test_create_model_purchase_returns_model_purchase(self):
        self.mock_mercadopago_repository.get_payment_data.return_value = Payment(
            payment_id=1,
            payment_data={"transaction_details": {"net_received_amount": 100}}
        )

        self.test_db.session.query.return_value\
            .filter.return_value\
            .filter.return_value\
            .first.return_value = MOCK_MODEL_MODEL

        response = self.model_repository.create_model_purchase(
            model_id=1,
            payment_id=2,
            printer_id=3,
        )

        assert isinstance(response, ModelPurchase)
        assert response.model.id == MOCK_MODEL_MODEL.id
        assert self.test_db.session.add.call_count == 2
        self.test_db.session.commit.assert_called_once()

    def test_create_model_purchase_rollbacks_and_refunds_payment_on_error(self):
        self.mock_mercadopago_repository.get_payment_data.return_value = Payment(
            payment_id=1,
            payment_data={"transaction_details": {"net_received_amount": 100}}
        )

        self.test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_MODEL_MODEL

        self.test_db.session.commit.side_effect = Exception("unexpected_error")

        with pytest.raises(Exception):
            self.model_repository.create_model_purchase(
                model_id=1,
                payment_id=2,
                printer_id=3,
            )

        self.test_db.session.rollback.assert_called_once()
        self.mock_mercadopago_repository.refund_payment.assert_called_once_with(2)

    def test_get_model_detail_returns_model_detail_with_user_liked_information_if_user_id_was_provided_and_user_likes_model(self):
        # Mock get model by id query
        self.test_db.session.query.return_value \
            .filter.return_value \
            .filter.return_value \
            .options.return_value \
            .first.return_value = MOCK_MODEL_MODEL

        # Mock get model like query
        self.test_db.session.query.return_value \
            .filter.return_value \
            .filter.return_value \
            .first.return_value = MOCK_MODEL_MODEL

        response = self.model_repository.get_model_detail(model_id=1, user_id=2)

        assert isinstance(response, Model)
        assert response.id == MOCK_MODEL_MODEL.id
        assert response.liked_by_user == True

    def test_get_model_detail_returns_model_detail_with_user_liked_information_if_user_id_was_provided_and_user_does_not_like_model(self):
        # Mock get model by id query
        self.test_db.session.query.return_value \
            .filter.return_value \
            .filter.return_value \
            .options.return_value \
            .first.return_value = MOCK_MODEL_MODEL

        # Mock get model like query
        self.test_db.session.query.return_value \
            .filter.return_value \
            .filter.return_value \
            .first.return_value = None

        response = self.model_repository.get_model_detail(model_id=1, user_id=2)

        assert isinstance(response, Model)
        assert response.id == MOCK_MODEL_MODEL.id
        assert response.liked_by_user == False

    @patch('my_app.api.repositories.model_repository.paginate')
    def test_get_printer_model_purchases_returns_model_purchase_page(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_MODEL_PURCHASE_MODEL]

        response = self.model_repository.get_printer_model_purchases(1, MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

    @patch('my_app.api.repositories.model_repository.paginate')
    def test_get_models_returns_models_with_like_information_if_user_id_was_provided(self, paginate_mock):
        liked_model = copy.deepcopy(MOCK_MODEL_MODEL)
        liked_model.id = 99
        unliked_model = copy.deepcopy(MOCK_MODEL_MODEL)
        unliked_model.id = 88

        mock_user_like_model = copy.deepcopy(MOCK_MODEL_LIKE_MODEL)
        mock_user_like_model.model_id = liked_model.id
        mock_user_like_model.user_id = 1000

        paginate_mock.return_value.all.return_value = [liked_model, unliked_model]

        # Mock user likes
        self.test_db.session.query.return_value \
            .filter.return_value \
            .filter.return_value \
            .all.return_value = [mock_user_like_model]

        response = self.model_repository.get_models(MOCK_FILTERS, 1000)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

        assert len(response.data) == 2
        assert response.data[0].id == 99
        assert response.data[0].liked_by_user is True
        assert response.data[1].id == 88
        assert response.data[1].liked_by_user is False

    @patch('my_app.api.repositories.model_repository.paginate')
    def test_get_models_returns_models_without_like_information_if_user_id_was_not_provided(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_MODEL_MODEL, MOCK_MODEL_MODEL]

        response = self.model_repository.get_models(MOCK_FILTERS, None)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

        assert len(response.data) == 2
        assert response.data[0].liked_by_user is None
        assert response.data[1].liked_by_user is None

    @patch('my_app.api.repositories.model_repository.paginate')
    def test_get_models_returns_models_with_like_information_if_user_id_was_provided(self, paginate_mock):
        paginate_mock.return_value.all.return_value = [MOCK_MODEL_MODEL]

        response = self.model_repository.get_designer_models(1, MOCK_FILTERS)

        assert isinstance(response, Page)
        assert response.page == MOCK_FILTERS["page"]
        assert response.page_size == MOCK_FILTERS["page_size"]
        paginate_mock.return_value.all.assert_called_once()

    def test_delete_model_success(self):
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = MOCK_MODEL_MODEL

        self.model_repository.delete_model(1, 2)

        self.test_db.session.commit.assert_called_once()

    def test_delete_model_throws_error_when_model_is_not_found(self):
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            self.model_repository.delete_model(1, 2)

        self.test_db.session.commit.assert_not_called()

    def test_delete_model_throws_error_when_model_is_not_owned_by_user(self):
        mock_model = copy.deepcopy(MOCK_MODEL_MODEL)
        mock_model.designer_id = 99
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = mock_model

        with pytest.raises(BusinessException):
            self.model_repository.delete_model(1, 2)

        self.test_db.session.commit.assert_not_called()

    def test_get_model_by_id_returns_model(self):
        # Mock get model by id query
        self.test_db.session.query.return_value \
            .filter.return_value \
            .filter.return_value \
            .first.return_value = MOCK_MODEL_MODEL

        response = self.model_repository.get_model_by_id(model_id=1)

        assert isinstance(response, Model)
        assert response.id == MOCK_MODEL_MODEL.id

    def test_get_model_purchase_from_printer_returns_model_purchase(self):
        self.test_db.session.query.return_value.join.return_value \
            .filter.return_value \
            .filter.return_value \
            .options.return_value \
            .first.return_value = MOCK_MODEL_PURCHASE_MODEL

        response = self.model_repository.get_model_purchase_from_printer(model_id=1, printer_id=2)

        assert isinstance(response, ModelPurchase)
        assert response.id == MOCK_MODEL_PURCHASE_MODEL.id

    def test_get_model_purchase_throws_error_when_purchase_does_not_exist(self):
        self.test_db.session.query.return_value.join.return_value \
            .filter.return_value \
            .filter.return_value \
            .options.return_value \
            .first.return_value = None

        with pytest.raises(NotFoundException):
            self.model_repository.get_model_purchase_from_printer(model_id=1, printer_id=2)
