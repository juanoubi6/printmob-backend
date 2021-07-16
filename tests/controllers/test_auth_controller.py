import json
import unittest
from unittest.mock import patch

from my_app.api import create_app
from tests.test_utils.mock_entities import MOCK_BUYER, MOCK_PRINTER
from tests.test_utils.test_json import LOGIN_RESPONSE_JSON, CREATE_PRINTER_JSON_REQUEST, CREATE_BUYER_JSON_REQUEST

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestAuthController(unittest.TestCase):

    @patch.object(app.auth_controller, "auth_service")
    def test_login_returns_user_data_on_success(self, mock_auth_service):
        mock_auth_service.get_user_login_data.return_value = (MOCK_BUYER, "JWT")

        res = client.post("/auth/login", data=json.dumps({"token": "test_token"}))
        assert res.status_code == 200
        assert res.json == LOGIN_RESPONSE_JSON

        mock_auth_service.get_user_login_data.assert_called_once_with("test_token")

    def test_login_returns_401_if_token_was_not_provided(self):
        res = client.post("/auth/login", data=json.dumps({}))
        assert res.status_code == 401

    @patch.object(app.auth_controller, "user_service")
    def test_create_printer_returns_201_on_success(self, mock_user_service):
        mock_user_service.create_printer.return_value = MOCK_PRINTER

        res = client.post("/auth/signup/printer", data=json.dumps(CREATE_PRINTER_JSON_REQUEST))

        assert res.status_code == 201
        mock_user_service.create_printer.assert_called_once()

    @patch.object(app.auth_controller, "user_service")
    def test_create_buyer_returns_201_on_success(self, mock_user_service):
        mock_user_service.create_buyer.return_value = MOCK_BUYER

        res = client.post("/auth/signup/buyer", data=json.dumps(CREATE_BUYER_JSON_REQUEST))

        assert res.status_code == 201
        mock_user_service.create_buyer.assert_called_once()
