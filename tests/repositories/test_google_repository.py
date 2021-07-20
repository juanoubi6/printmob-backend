import os
import unittest
from concurrent.futures import TimeoutError
from unittest.mock import patch, Mock

import pytest
import requests

from my_app.api.exceptions import GoogleValidationException
from my_app.api.repositories import GoogleRepository

client_id = os.environ["GOOGLE_CLIENT_ID"]
google_fallback_url = os.environ["GOOGLE_AUTH_FALLBACK_URL"]


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.mock_executor = Mock()
        self.google_repository = GoogleRepository(client_id, google_fallback_url, self.mock_executor)

    def test_retrieve_token_data_returns_google_user_data_on_default_flow_success(self):
        # Mock default method ok
        mock_future = Mock()
        self.mock_executor.submit.return_value = mock_future
        mock_future.result.return_value = GOOGLE_RESPONSE_MOCK

        google_user_data = self.google_repository.retrieve_token_data("token")

        assert google_user_data.first_name == GOOGLE_RESPONSE_MOCK["given_name"]
        assert google_user_data.last_name == GOOGLE_RESPONSE_MOCK["family_name"]
        assert google_user_data.picture == GOOGLE_RESPONSE_MOCK["picture"]
        assert google_user_data.email == GOOGLE_RESPONSE_MOCK["email"]

    @patch('my_app.api.repositories.google_repository.requests')
    def test_retrieve_token_data_returns_data_using_fallback_flow_when_default_method_timeouts(self, requests_mock):
        ok_response = Mock()
        ok_response.status_code = 200
        ok_response.json.return_value = GOOGLE_RESPONSE_MOCK

        # Mock default method timeout
        mock_future = Mock()
        self.mock_executor.submit.return_value = mock_future
        mock_future.result.side_effect = TimeoutError()

        # Fallback works ok
        requests_mock.get.return_value = ok_response

        google_user_data = self.google_repository.retrieve_token_data("token")

        assert google_user_data.email == GOOGLE_RESPONSE_MOCK["email"]

    def test_retrieve_token_data_raises_exception_if_default_flow_fails(self):
        mock_future = Mock()
        self.mock_executor.submit.return_value = mock_future
        mock_future.result.side_effect = Exception("Something happened")

        with pytest.raises(GoogleValidationException):
            self.google_repository.retrieve_token_data("token")

    @patch('my_app.api.repositories.google_repository.requests')
    def test_retrieve_token_data_raises_exception_if_fallback_flow_fails(self, requests_mock):
        bad_response = Mock()
        bad_response.status_code = 400
        bad_response.json.return_value = {
            "error": "error",
            "error_description": "error_desc"
        }

        # Default method fails because of timeout
        mock_future = Mock()
        self.mock_executor.submit.return_value = mock_future
        mock_future.result.side_effect = TimeoutError()

        # Fallback method fails
        requests_mock.get.return_value = bad_response

        with pytest.raises(GoogleValidationException):
            self.google_repository.retrieve_token_data("token")


GOOGLE_RESPONSE_MOCK = {
    "iss": "accounts.google.com",
    "azp": "810426611199-go18jjitmdhrtm9bg00uk7n583cl1ncm.apps.googleusercontent.com",
    "aud": client_id,
    "sub": "110715879182890833924",
    "email": "juan.manuel.oubina@gmail.com",
    "email_verified": "true",
    "at_hash": "WpjYUVdiQonG8_J1FcLxUw",
    "name": "Juan Manuel Oubiña",
    "picture": "https://lh3.googleusercontent.com/a-/AOh14Gi9qSp_vM7EEBu4RCAUtksHI72OW1f8B_NhA88GmA=s96-c",
    "given_name": "Juan Manuel",
    "family_name": "Oubiña",
    "locale": "es",
    "iat": "1625421874",
    "exp": "9999999999",
    "jti": "e9734723094994cab2be700f89dc8e0d635fd615",
    "alg": "RS256",
    "kid": "b6f8d55da534ea91cb2cb00e1af4e8e0cdeca93d",
    "typ": "JWT"
}

MOCK_REQUEST_RESPONSE = requests.Response()
