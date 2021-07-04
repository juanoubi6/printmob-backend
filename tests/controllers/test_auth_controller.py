import json
import unittest
from unittest.mock import patch

from my_app.api import create_app
from tests.utils.mock_entities import MOCK_ORDER, MOCK_PRINTER_USER, MOCK_BUYER
from tests.utils.test_json import UPDATE_ORDER_STATUSES_MASSIVE_REQUEST_JSON, UPDATE_ORDER_REQUEST_JSON, \
    UPDATE_ORDER_RESPONSE_JSON, LOGIN_RESPONSE_JSON

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
