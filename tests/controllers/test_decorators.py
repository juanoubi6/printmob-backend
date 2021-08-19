import os
import unittest

from my_app.api import create_app
from my_app.api.controllers.decorators import validate_bearer_token
from my_app.api.utils.token_manager import TokenManager

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


@app.route('/decorator-endpoint', methods=['GET'])
@validate_bearer_token
def decorator_endpoint(user_data):
    return user_data, 200


class TestDecorators(unittest.TestCase):

    def test_endpoint_returns_401_when_token_is_not_present(self):
        res = client.get("/decorator-endpoint", headers={})
        assert res.status_code == 401
        assert res.json["message"] == "El token de autenticación no ha sido enviado"

    def test_endpoint_returns_401_when_token_is_not_valid(self):
        res = client.get("/decorator-endpoint", headers={"Authorization": "malformed"})
        assert res.status_code == 401
        assert res.json["message"] == "Ocurrió un problema al validar tu token de autenticación: Not enough segments"

    def test_endpoint_returns_200_when_token_is_valid(self):
        token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])
        valid_token = token_manager.get_token_from_payload({"some": "payload"})

        res = client.get("/decorator-endpoint", headers={"Authorization": valid_token})
        assert res.status_code == 200
        assert "some" in res.json
