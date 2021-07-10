import os
import os
import unittest
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.utils.token_manager import TokenManager
from tests.test_utils.mock_entities import MOCK_BUYER, MOCK_PRINTER
from tests.test_utils.test_json import GET_PRINTER_PROFILE_RESPONSE_JSON, GET_BUYER_PROFILE_RESPONSE_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestUserController(unittest.TestCase):

    def setUp(self):
        token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])
        self.printer_authorization_token = token_manager.get_token_from_payload(MOCK_PRINTER.identity_data())
        self.buyer_authorization_token = token_manager.get_token_from_payload(MOCK_BUYER.identity_data())

    def test_user_profile_endpoint_returns_401_when_token_is_not_present(self):
        res = client.get("/users/1/profile", headers={})
        assert res.status_code == 401
        assert res.json["message"] == "Missing Authentication token"

    @patch.object(app.user_controller, "user_service")
    def test_ger_user_profile_returns_printer_data_when_printer_token_is_provided(self, mock_user_service):
        mock_user_service.get_printer_by_email.return_value = MOCK_PRINTER

        res = client.get(
            "/users/{}/profile".format(MOCK_PRINTER.id),
            headers={"Authorization": self.printer_authorization_token}
        )

        assert res.status_code == 200
        assert res.json == GET_PRINTER_PROFILE_RESPONSE_JSON

        mock_user_service.get_printer_by_email.assert_called_once_with(MOCK_PRINTER.email)

    @patch.object(app.user_controller, "user_service")
    def test_ger_user_profile_returns_buyer_data_when_printer_token_is_provided(self, mock_user_service):
        mock_user_service.get_buyer_by_email.return_value = MOCK_BUYER

        res = client.get(
            "/users/{}/profile".format(MOCK_BUYER.id),
            headers={"Authorization": self.buyer_authorization_token}
        )

        assert res.status_code == 200
        assert res.json == GET_BUYER_PROFILE_RESPONSE_JSON

        mock_user_service.get_buyer_by_email.assert_called_once_with(MOCK_BUYER.email)

    def test_ger_user_profile_returns_401_if_requested_user_id_information_does_not_match_token_id(self):
        res = client.get(
            "/users/99/profile",
            headers={"Authorization": self.buyer_authorization_token}
        )

        assert res.status_code == 401
        assert res.json["message"] == "Identified user and user_id do not match"
