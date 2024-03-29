import io
import json
import os
import unittest
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.domain import Page
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException
from my_app.api.utils.token_manager import TokenManager
from tests.test_utils.mock_entities import MOCK_CAMPAIGN, MOCK_CAMPAIGN_MODEL_IMAGE, MOCK_ORDER, MOCK_PRINTER, \
    MOCK_DESIGNER, MOCK_CAMPAIGN_WITH_ALLIANCE_DATA
from tests.test_utils.test_json import CAMPAIGN_GET_RESPONSE_JSON, CAMPAIGN_POST_REQUEST_JSON, \
    CAMPAIGN_POST_RESPONSE_JSON, \
    CAMPAIGN_MODEL_IMAGE_JSON, CAMPAIGN_FROM_MODEL_POST_REQUEST_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestCampaignController(unittest.TestCase):

    def setUp(self):
        token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])
        self.printer_authorization_token = token_manager.get_token_from_payload(MOCK_PRINTER.identity_data())
        self.designer_authorization_token = token_manager.get_token_from_payload(MOCK_DESIGNER.identity_data())

    @patch.object(app.campaign_controller, "campaign_service")
    def test_post_campaign_returns_campaign(self, mock_campaign_service):
        mock_campaign_service.create_campaign.return_value = MOCK_CAMPAIGN

        res = client.post("/campaigns", data=json.dumps(CAMPAIGN_POST_REQUEST_JSON),
                          headers={"Authorization": self.printer_authorization_token})
        assert res.status_code == 201
        assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_POST_RESPONSE_JSON

    @patch.object(app.campaign_controller, "campaign_service")
    def test_post_campaign_returns_422_if_unprocessable_entity_error_occurs(self, mock_campaign_service):
        mock_campaign_service.create_campaign.side_effect = UnprocessableEntityException("some error")

        res = client.post("/campaigns", data=json.dumps(CAMPAIGN_POST_REQUEST_JSON),
                          headers={"Authorization": self.printer_authorization_token})
        assert res.status_code == 422
        assert res.json['error:'] == "Unprocessable entity error"
        assert res.json['message'] == "some error"

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_campaigns_returns_campaign_page(self, mock_campaign_service):
        mock_campaign_service.get_campaigns.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_CAMPAIGN]
        )

        res = client.get("/campaigns?page=1&page_size=10")
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_CAMPAIGN.id

    def test_get_campaigns_fails_on_invalid_pagination_params(self):
        res = client.get("/campaigns?page=1&page_size=-10")

        assert res.status_code == 400
        assert res.json["message"] == "El query param 'page_size' debe ser un número"

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_campaign_detail_returns_campaign_json(self, mock_campaign_service):
        mock_campaign_service.get_campaign_detail.return_value = MOCK_CAMPAIGN

        res = client.get("/campaigns/1", headers={"Authorization": self.printer_authorization_token})
        assert res.status_code == 200
        assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_GET_RESPONSE_JSON

    @patch.object(app.campaign_controller, "campaign_service")
    def test_create_campaign_model_image_returns_200(self, mock_campaign_service):
        mock_campaign_service.create_campaign_model_image.return_value = MOCK_CAMPAIGN_MODEL_IMAGE

        res = client.post(
            "/campaigns/1/model-images",
            data={'image': (io.BytesIO(b"someImageData"), 'testImageName.jpg')},
            content_type='multipart/form-data',
            headers={"Authorization": self.printer_authorization_token}
        )

        assert res.status_code == 201
        assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_MODEL_IMAGE_JSON
        mock_campaign_service.create_campaign_model_image.assert_called_once()

        called_file = mock_campaign_service.create_campaign_model_image.call_args[0][1]
        assert called_file.content == bytes(b"someImageData")
        assert called_file.mimetype == "image/jpeg"

    @patch.object(app.campaign_controller, "campaign_service")
    def test_delete_campaign_model_image_returns_200_on_success(self, mock_campaign_service):
        res = client.delete("/campaigns/1/model-images/2")

        assert res.status_code == 200
        mock_campaign_service.delete_campaign_model_image.assert_called_once_with(2)

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_campaign_orders_returns_orders_page(self, mock_campaign_service):
        mock_campaign_service.get_campaign_orders.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_ORDER]
        )

        res = client.get("/campaigns/1/orders?page=1&page_size=10")
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_ORDER.id

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_buyer_campaigns_returns_campaign_page(self, mock_campaign_service):
        mock_campaign_service.get_buyer_campaigns.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_CAMPAIGN]
        )

        res = client.get("/buyers/1/campaigns?page=1&page_size=10")
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_CAMPAIGN.id

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_designer_campaigns_returns_campaign_page(self, mock_campaign_service):
        mock_campaign_service.get_designer_campaigns.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_CAMPAIGN]
        )

        res = client.get("/designers/1/campaigns?page=1&page_size=10",
                         headers={"Authorization": self.designer_authorization_token})
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_CAMPAIGN.id

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_designer_campaigns_returns_campaign_page_with_alliance_percentage_data(self, mock_campaign_service):
        mock_campaign_service.get_designer_campaigns.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_CAMPAIGN_WITH_ALLIANCE_DATA]
        )

        res = client.get("/designers/1/campaigns?page=1&page_size=10",
                         headers={"Authorization": self.designer_authorization_token})
        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_CAMPAIGN.id
        assert res.json["data"][0]["alliance_percentages"]["printer_percentage"] == \
               MOCK_CAMPAIGN_WITH_ALLIANCE_DATA.alliance_percentages["printer_percentage"]
        assert res.json["data"][0]["alliance_percentages"]["designer_percentage"] == \
               MOCK_CAMPAIGN_WITH_ALLIANCE_DATA.alliance_percentages["designer_percentage"]

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_designer_campaigns_fails_if_designer_id_does_not_match_token_id(self, mock_campaign_service):
        mock_campaign_service.get_designer_campaigns.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_CAMPAIGN]
        )

        res = client.get("/designers/99/campaigns?page=1&page_size=10",
                         headers={"Authorization": self.designer_authorization_token})

        assert res.status_code == 400

    @patch.object(app.campaign_controller, "campaign_service")
    def test_cancel_campaign_returns_200_on_success(self, mock_campaign_service):
        res = client.delete("/campaigns/1")

        assert res.status_code == 200
        mock_campaign_service.cancel_campaign.assert_called_once_with(1)

    @patch.object(app.campaign_controller, "campaign_service")
    def test_create_campaign_with_model_returns_campaign(self, mock_campaign_service):
        mock_campaign_service.create_campaign_from_model.return_value = MOCK_CAMPAIGN

        res = client.post("/campaigns/from-model", data=json.dumps(CAMPAIGN_FROM_MODEL_POST_REQUEST_JSON),
                          headers={"Authorization": self.printer_authorization_token})

        assert res.status_code == 201
        assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_POST_RESPONSE_JSON
