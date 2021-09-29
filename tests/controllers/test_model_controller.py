import copy
import io
import json
import os
import unittest
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.domain import Page, ModelOrdering
from my_app.api.utils.token_manager import TokenManager
from tests.test_utils.mock_entities import MOCK_DESIGNER, MOCK_MODEL, MOCK_PRINTER, MOCK_MODEL_IMAGE, \
    MOCK_MODEL_CATEGORY, MOCK_MODEL_LIKE, MOCK_MODEL_PURCHASE
from tests.test_utils.test_json import CREATE_MODEL_REQUEST, CREATE_MODEL_RESPONSE_JSON, MODEL_IMAGE_JSON, \
    GET_USER_LIKED_MODEL_DETAIL_JSON_RESPONSE, GET_NEUTRAL_MODEL_DETAIL_JSON_RESPONSE

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestModelController(unittest.TestCase):

    def setUp(self):
        token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])
        self.designer_authorization_token = token_manager.get_token_from_payload(MOCK_DESIGNER.identity_data())
        self.printer_authorization_token = token_manager.get_token_from_payload(MOCK_PRINTER.identity_data())

    @patch.object(app.model_controller, "model_service")
    def test_create_model_returns_model(self, mock_model_service):
        mock_model_service.create_model.return_value = MOCK_MODEL

        res = client.post(
            "/models",
            data=CREATE_MODEL_REQUEST,
            content_type='multipart/form-data',
            headers={"Authorization": self.designer_authorization_token}
        )

        assert res.status_code == 201
        assert json.loads(res.data.decode("utf-8")) == CREATE_MODEL_RESPONSE_JSON

    def test_create_model_fails_if_call_user_is_not_a_designer(self):
        res = client.post(
            "/models",
            data={},
            content_type='multipart/form-data',
            headers={"Authorization": self.printer_authorization_token}
        )

        assert res.status_code == 400
        assert res.json["message"] == "Solo los diseñadores pueden crear modelos"

    @patch.object(app.model_controller, "model_service")
    def test_create_model_image_returns_200(self, mock_model_service):
        mock_model_service.create_model_image.return_value = MOCK_MODEL_IMAGE

        res = client.post(
            "/models/1/images",
            data={'image': (io.BytesIO(b"someImageData"), 'testImageName.jpg')},
            content_type='multipart/form-data',
            headers={"Authorization": self.designer_authorization_token}
        )

        assert res.status_code == 201
        assert json.loads(res.data.decode("utf-8")) == MODEL_IMAGE_JSON
        mock_model_service.create_model_image.assert_called_once()

        called_file = mock_model_service.create_model_image.call_args[0][1]
        assert called_file.content == bytes(b"someImageData")
        assert called_file.mimetype == "image/jpeg"

    @patch.object(app.model_controller, "model_service")
    def test_delete_model_image_returns_200_on_success(self, mock_model_service):
        res = client.delete("/models/1/images/2", headers={"Authorization": self.designer_authorization_token})

        assert res.status_code == 200
        mock_model_service.delete_model_image.assert_called_once_with(2)

    @patch.object(app.model_controller, "model_service")
    def test_get_model_categories_return_model_category_list(self, mock_model_service):
        mock_model_service.get_model_categories.return_value = [MOCK_MODEL_CATEGORY]

        res = client.get("/models/categories")

        assert res.status_code == 200
        assert res.json == [{'id': 1, 'name': 'Categoria 1'}]

    @patch.object(app.model_controller, "model_service")
    def test_add_like_to_model_returns_like(self, mock_model_service):
        mock_model_service.add_like_to_model.return_value = MOCK_MODEL_LIKE

        res = client.post("/models/3/likes", headers={"Authorization": self.designer_authorization_token})

        assert res.status_code == 201
        assert res.json == {'id': 1, 'user_id': MOCK_MODEL_LIKE.user_id, "model_id": MOCK_MODEL_LIKE.model_id}
        mock_model_service.add_like_to_model.assert_called_once_with(3, MOCK_DESIGNER.id)

    @patch.object(app.model_controller, "model_service")
    def test_remove_like_from_model_removes_like(self, mock_model_service):
        res = client.delete(
            "/models/1/likes",
            headers={"Authorization": self.designer_authorization_token}
        )

        assert res.status_code == 200
        mock_model_service.remove_like_from_model.assert_called_once_with(1, MOCK_DESIGNER.id)

    @patch.object(app.model_controller, "model_service")
    def test_create_model_purchase_returns_created_model_purchase(self, mock_model_service):
        mock_model_service.create_model_purchase.return_value = MOCK_MODEL_PURCHASE

        res = client.post("/models/purchases",
                          data=json.dumps({
                              "model_id": 1,
                              "mp_payment_id": 2
                          }),
                          headers={"Authorization": self.printer_authorization_token})

        assert res.status_code == 201
        assert res.json["id"] == MOCK_MODEL_PURCHASE.id

    def test_create_model_purchase_fails_when_model_id_is_not_provided(self):
        res = client.post("/models/purchases",
                          data=json.dumps({
                              "mp_payment_id": 2
                          }),
                          headers={"Authorization": self.printer_authorization_token})

        assert res.status_code == 400
        assert res.json["message"] == "El ID del modelo no fue provisto"

    def test_create_model_purchase_fails_when_payment_id_is_not_provided(self):
        res = client.post("/models/purchases",
                          data=json.dumps({
                              "model_id": 2
                          }),
                          headers={"Authorization": self.printer_authorization_token})

        assert res.status_code == 400
        assert res.json["message"] == "El ID del pago no fue provisto"

    @patch.object(app.model_controller, "model_service")
    def test_get_printer_model_purchase_returns_model_purchase_page(self, mock_model_service):
        mock_model_service.get_printer_model_purchases.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_MODEL_PURCHASE]
        )

        res = client.get(
            "/models/printers/purchases?page=1&page_size=10&category_id=1",
            headers={"Authorization": self.printer_authorization_token}
        )
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_MODEL_PURCHASE.id

    def test_get_printer_model_purchase_fails_if_user_is_not_a_printer(self):
        res = client.get(
            "/models/printers/purchases?page=1&page_size=10&category_id=1",
            headers={"Authorization": self.designer_authorization_token}
        )

        assert res.status_code == 400
        assert res.json["message"] == "Solo los impresores pueden acceder a esta información"

    @patch.object(app.model_controller, "model_service")
    def test_get_model_detail_is_called_with_user_id_auth_token_is_provided_and_returns_model_detail_with_liked_user_info(
            self, mock_model_service
    ):
        user_liked_model = copy.deepcopy(MOCK_MODEL)
        user_liked_model.liked_by_user = True
        mock_model_service.get_model_detail.return_value = user_liked_model

        res = client.get("/models/99", headers={"Authorization": self.designer_authorization_token})

        assert res.status_code == 200
        assert res.json == GET_USER_LIKED_MODEL_DETAIL_JSON_RESPONSE
        mock_model_service.get_model_detail.assert_called_once_with(99, MOCK_DESIGNER.id)

    @patch.object(app.model_controller, "model_service")
    def test_get_model_detail_is_called_without_user_id_auth_token_is_not_provided_and_returns_model_detail(
            self, mock_model_service
    ):
        neutral_model = copy.deepcopy(MOCK_MODEL)
        neutral_model.liked_by_user = None
        mock_model_service.get_model_detail.return_value = neutral_model

        res = client.get("/models/99")

        assert res.status_code == 200
        assert res.json == GET_NEUTRAL_MODEL_DETAIL_JSON_RESPONSE
        mock_model_service.get_model_detail.assert_called_once_with(99, None)

    @patch.object(app.model_controller, "model_service")
    def test_get_model_ordering_return_model_ordering_list(self, mock_model_service):
        mock_model_service.get_model_ordering.return_value = [ModelOrdering("value", "name")]

        res = client.get("/models/ordering")

        assert res.status_code == 200
        assert res.json == [{'value': "value", 'name': 'name'}]

    @patch.object(app.model_controller, "model_service")
    def test_get_models_returns_models(self, mock_model_service):
        mock_model_service.get_models.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_MODEL]
        )

        res = client.get(
            "/models?page=1&page_size=10&category_id=1&order=MOST_RECENT",
            headers={"Authorization": self.printer_authorization_token}
        )
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_MODEL_PURCHASE.id

    @patch.object(app.model_controller, "model_service")
    def test_get_designer_models_returns_models(self, mock_model_service):
        mock_model_service.get_designer_models.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_MODEL]
        )

        res = client.get(
            "/designers/{id}/models?page=1&page_size=10&category_id=1&order=MOST_RECENT".format(id=MOCK_DESIGNER.id),
            headers={"Authorization": self.designer_authorization_token}
        )
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_MODEL_PURCHASE.id

    @patch.object(app.model_controller, "model_service")
    def test_delete_model_returns_200_on_success(self, mock_model_service):
        res = client.delete("/models/1", headers={"Authorization": self.designer_authorization_token})

        assert res.status_code == 200
        mock_model_service.delete_model.assert_called_once_with(1, MOCK_DESIGNER.id)

    @patch.object(app.model_controller, "model_service")
    def test_get_model_purchase_from_printer_returns_model_purchase(self, mock_model_service):
        mock_model_service.get_model_purchase_from_printer.return_value = MOCK_MODEL_PURCHASE

        res = client.get("/models/1/purchase", headers={"Authorization": self.printer_authorization_token})

        assert res.status_code == 200
        mock_model_service.get_model_purchase_from_printer.assert_called_once_with(1, MOCK_PRINTER.id)
