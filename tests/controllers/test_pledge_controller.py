import json
import os
import unittest
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.utils.token_manager import TokenManager
from tests.test_utils.mock_entities import MOCK_PLEDGE, MOCK_BUYER
from tests.test_utils.test_json import GET_PLEDGES_RESPONSE_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestPledgeController(unittest.TestCase):

    def setUp(self):
        token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])
        self.buyer_authorization_token = token_manager.get_token_from_payload(MOCK_BUYER.identity_data())

    @patch.object(app.pledge_controller, "pledge_service")
    def test_cancel_pledge_returns_200_on_success(self, mock_pledge_service):
        res = client.delete("/pledges/1", headers={"Authorization": self.buyer_authorization_token})

        assert res.status_code == 200
        mock_pledge_service.cancel_pledge.assert_called_once_with(1)

    @patch.object(app.pledge_controller, "pledge_service")
    def test_get_pledges_returns_200_on_success(self, mock_pledge_service):
        mock_pledge_service.get_pledges.return_value = [MOCK_PLEDGE]

        res = client.get("/pledges?buyer_id=1&campaign_id=2")

        assert res.status_code == 200
        assert res.json == GET_PLEDGES_RESPONSE_JSON
        mock_pledge_service.get_pledges.assert_called_once()

        called_filters = mock_pledge_service.get_pledges.mock_calls[0][1][0]
        assert "campaign_id" in called_filters
        assert "buyer_id" in called_filters

    @patch.object(app.pledge_controller, "pledge_service")
    def test_create_pledge_with_payment_returns_created_pledge(self, mock_pledge_service):
        mock_pledge_service.create_pledge_with_payment.return_value = MOCK_PLEDGE

        res = client.post("/pledges/payment",
                          data=json.dumps({
                              "campaign_id": 1,
                              "mp_payment_id": 2
                          }),
                          headers={"Authorization": self.buyer_authorization_token})

        assert res.status_code == 201
        assert res.json["id"] == MOCK_PLEDGE.id

    def test_create_pledge_with_payment_fails_when_campaign_id_is_not_provided(self):
        res = client.post("/pledges/payment",
                          data=json.dumps({
                              "mp_payment_id": 2
                          }),
                          headers={"Authorization": self.buyer_authorization_token})

        assert res.status_code == 400
        assert res.json["message"] == "El ID de la campaña no fue provisto"

    def test_create_pledge_with_payment_fails_when_payment_id_is_not_provided(self):
        res = client.post("/pledges/payment",
                          data=json.dumps({
                              "campaign_id": 2
                          }),
                          headers={"Authorization": self.buyer_authorization_token})

        assert res.status_code == 400
        assert res.json["message"] == "El ID del pago no fue provisto"
