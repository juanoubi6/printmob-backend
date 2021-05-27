import unittest
from unittest.mock import Mock

from my_app.api import create_app
from my_app.api.domain import Campaign

app = create_app()
app.testing = True
client = app.test_client()


class TestCampaignController(unittest.TestCase):

    def test_get_campaigns_returns_campaign_list(self):
        mock_campaign_service = Mock()
        mock_campaign_service.get_campaigns.return_value = [Campaign("5555",1)]
        app.campaign_controller.campaign_service = mock_campaign_service

        res = client.get("/campaigns")
        self.assertEqual(res.json[0]["name"], "5555")
