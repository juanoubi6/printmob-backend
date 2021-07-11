import io
import json
import unittest
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.domain import Page
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException
from tests.test_utils.mock_entities import MOCK_CAMPAIGN, MOCK_CAMPAIGN_MODEL_IMAGE, MOCK_ORDER
from tests.test_utils.test_json import CAMPAIGN_GET_RESPONSE_JSON, CAMPAIGN_POST_REQUEST_JSON, CAMPAIGN_POST_RESPONSE_JSON, \
    CAMPAIGN_MODEL_IMAGE_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestCampaignController(unittest.TestCase):

    @patch.object(app.campaign_controller, "campaign_service")
    def test_post_campaign_returns_campaign(self, mock_campaign_service):
        mock_campaign_service.create_campaign.return_value = MOCK_CAMPAIGN

        res = client.post("/campaigns", data=json.dumps(CAMPAIGN_POST_REQUEST_JSON))
        assert res.status_code == 201
        assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_POST_RESPONSE_JSON

    @patch.object(app.campaign_controller, "campaign_service")
    def test_post_campaign_returns_422_if_unprocessable_entity_error_occurs(self, mock_campaign_service):
        mock_campaign_service.create_campaign.side_effect = UnprocessableEntityException("some error")

        res = client.post("/campaigns", data=json.dumps(CAMPAIGN_POST_REQUEST_JSON))
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
        assert res.json["message"] == "The query param 'page_size' should be numeric"

    @patch.object(app.campaign_controller, "campaign_service")
    def test_get_campaign_detail_returns_campaign_json(self, mock_campaign_service):
        mock_campaign_service.get_campaign_detail.return_value = MOCK_CAMPAIGN

        res = client.get("/campaigns/1")
        assert res.status_code == 200
        assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_GET_RESPONSE_JSON

    @patch.object(app.campaign_controller, "campaign_service")
    def test_create_campaign_model_image_returns_200(self, mock_campaign_service):
        mock_campaign_service.create_campaign_model_image.return_value = MOCK_CAMPAIGN_MODEL_IMAGE

        res = client.post(
            "/campaigns/1/model-images",
            data={'image': (io.BytesIO(b"someImageData"), 'testImageName.jpg')},
            content_type='multipart/form-data'
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
