import json
from unittest.mock import patch

from tests.utils.mock_data import MOCK_CAMPAIGN
from tests.utils.test_json import CAMPAIGN_GET_RESPONSE_JSON, CAMPAIGN_POST_REQUEST_JSON, CAMPAIGN_POST_RESPONSE_JSON

from my_app.api import create_app
from my_app.api.domain import Page
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


@patch.object(app.campaign_controller, "campaign_service")
def test_post_campaign_returns_campaign(mock_campaign_service):
    mock_campaign_service.create_campaign.return_value = MOCK_CAMPAIGN

    res = client.post("/campaigns", data=json.dumps(CAMPAIGN_POST_REQUEST_JSON))
    assert res.status_code == 201
    assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_POST_RESPONSE_JSON


@patch.object(app.campaign_controller, "campaign_service")
def test_post_campaign_returns_422_if_unprocessable_entity_error_occurs(mock_campaign_service):
    mock_campaign_service.create_campaign.side_effect = UnprocessableEntityException("some error")

    res = client.post("/campaigns", data=json.dumps(CAMPAIGN_POST_REQUEST_JSON))
    assert res.status_code == 422
    assert res.json['error:'] == "Unprocessable entity error"
    assert res.json['message'] == "some error"


@patch.object(app.campaign_controller, "campaign_service")
def test_get_campaigns_returns_campaign_page(mock_campaign_service):
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


def test_get_campaigns_fails_on_invalid_pagination_params():
    res = client.get("/campaigns?page=1&page_size=-10")

    assert res.status_code == 400
    assert res.json["message"] == "The query param 'page_size' should be numeric"


@patch.object(app.campaign_controller, "campaign_service")
def test_get_campaign_detail_returns_campaign_json(mock_campaign_service):
    mock_campaign_service.get_campaign_detail.return_value = MOCK_CAMPAIGN

    res = client.get("/campaigns/1")
    assert res.status_code == 200
    assert json.loads(res.data.decode("utf-8")) == CAMPAIGN_GET_RESPONSE_JSON
