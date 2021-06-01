from unittest.mock import patch

from my_app.api import create_app
from my_app.api.domain import Campaign

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


@patch.object(app.campaign_controller, "campaign_service")
def test_get_campaigns_returns_campaign_list(mock_campaign_service):
    mock_campaign_service.get_campaigns.return_value = [Campaign("5555", 1)]

    res = client.get("/campaigns")
    assert res.json[0]["name"] == "5555"
