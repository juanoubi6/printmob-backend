from unittest.mock import patch

from my_app.api import create_app
from my_app.api.exceptions import BusinessException, ServerException

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


@patch.object(app.campaign_controller, "campaign_service")
def test_any_endpoint_returns_400_on_not_business_exception(mock_campaign_service):
    mock_campaign_service.get_campaign_detail.side_effect = BusinessException("not found")

    res = client.get("/campaigns/1")
    assert res.status_code == 400
    assert 'message' in res.json
    assert res.json['message'] == "not found"


@patch.object(app.campaign_controller, "campaign_service")
def test_any_endpoint_returns_500_on_server_exception(mock_campaign_service):
    mock_campaign_service.get_campaign_detail.side_effect = ServerException("some server error")

    res = client.get("/campaigns/1")
    assert res.status_code == 500
    assert 'message' in res.json
    assert res.json['message'] == "some server error"


@patch.object(app.campaign_controller, "campaign_service")
def test_any_endpoint_returns_500_on_unhandled_exception(mock_campaign_service):
    mock_campaign_service.get_campaign_detail.side_effect = Exception("some unhandler error")

    res = client.get("/campaigns/1")
    assert res.status_code == 500
    assert 'message' in res.json
    assert res.json['message'] == "some unhandler error"
