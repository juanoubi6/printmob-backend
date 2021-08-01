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
    def test_login_returns_user_data_on_success_and_cookie(self, mock_auth_service):
        mock_auth_service.get_user_login_data.return_value = (MOCK_BUYER, "JWT")

        res = client.post("/auth/login", data=json.dumps({"token": "test_token"}))
        assert res.status_code == 200
        assert res.json == LOGIN_RESPONSE_JSON
        assert res.headers.get("Set-Cookie") == "printmob-backend-cookie=JWT; Path=/"

        mock_auth_service.get_user_login_data.assert_called_once_with("test_token")

    def test_login_returns_400_if_token_was_not_provided(self):
        res = client.post("/auth/login", data=json.dumps({}))
        assert res.status_code == 400

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

    def test_validate_user_data_returns_400_when_username_or_email_are_missing(self):
        res = client.post("/auth/signup/validate", data=json.dumps({"email": "pepe@gmail.com"}))

        assert res.status_code == 400

    @patch.object(app.auth_controller, "user_service")
    def test_validate_user_data_returns_200_with_validation_results(self, mock_user_service):
        mock_user_service.validate_user_name_and_email_existence.return_value = {"email": True, "user_name": False}
        res = client.post("/auth/signup/validate", data=json.dumps({"email": "pepe@gmail.com", "user_name": "pepe"}))

        assert res.status_code == 200
        assert res.json["email"] is True
        assert res.json["user_name"] is False
