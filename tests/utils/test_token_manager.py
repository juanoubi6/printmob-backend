import os
import unittest

from my_app.api.utils.token_manager import TokenManager

token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])


class TestTokenManager(unittest.TestCase):

    def test_get_signed_token_payload_returns_payload(self):
        payload = {"some": "payload"}

        token = token_manager.get_token_from_payload(payload)
        decoded_payload = token_manager.get_payload_from_token(token)

        assert "some" in decoded_payload
        assert "exp" in decoded_payload

