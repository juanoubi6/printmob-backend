import unittest
from unittest.mock import Mock

import pytest

from my_app.api.exceptions import AuthException
from my_app.api.services import AuthService
from tests.test_utils.mock_entities import MOCK_GOOGLE_USER_DATA, MOCK_PRINTER_USER, MOCK_PRINTER, \
    MOCK_BUYER_USER, MOCK_BUYER


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.mock_google_repository = Mock()
        self.mock_user_repository = Mock()
        self.mock_token_manager = Mock()
        self.auth_service = AuthService(self.mock_google_repository, self.mock_user_repository, self.mock_token_manager)

    def test_get_user_login_data_returns_printer_data_on_printer_login(self):
        self.mock_google_repository.retrieve_token_data.return_value = MOCK_GOOGLE_USER_DATA
        self.mock_user_repository.get_user_by_email.return_value = MOCK_PRINTER_USER
        self.mock_user_repository.get_printer_by_email.return_value = MOCK_PRINTER
        self.mock_token_manager.get_token_from_payload.return_value = "signed_jwt"

        user, jwt = self.auth_service.get_user_login_data("auth_token")

        assert user == MOCK_PRINTER
        assert jwt == "signed_jwt"
        self.mock_google_repository.retrieve_token_data.assert_called_once_with("auth_token")
        self.mock_user_repository.get_user_by_email.assert_called_once_with(MOCK_GOOGLE_USER_DATA.email)
        self.mock_user_repository.get_printer_by_email.assert_called_once_with(MOCK_PRINTER_USER.email)
        self.mock_token_manager.get_token_from_payload.assert_called_once_with(MOCK_PRINTER.identity_data())

    def test_get_user_login_data_returns_buyer_data_on_buyer_login(self):
        self.mock_google_repository.retrieve_token_data.return_value = MOCK_GOOGLE_USER_DATA
        self.mock_user_repository.get_user_by_email.return_value = MOCK_BUYER_USER
        self.mock_user_repository.get_buyer_by_email.return_value = MOCK_BUYER
        self.mock_token_manager.get_token_from_payload.return_value = "signed_jwt"

        user, jwt = self.auth_service.get_user_login_data("auth_token")

        assert user == MOCK_BUYER
        assert jwt == "signed_jwt"
        self.mock_google_repository.retrieve_token_data.assert_called_once_with("auth_token")
        self.mock_user_repository.get_user_by_email.assert_called_once_with(MOCK_GOOGLE_USER_DATA.email)
        self.mock_user_repository.get_buyer_by_email.assert_called_once_with(MOCK_BUYER_USER.email)
        self.mock_token_manager.get_token_from_payload.assert_called_once_with(MOCK_BUYER.identity_data())

    def test_get_user_login_data_raises_exception_if_user_does_not_exist(self):
        self.mock_google_repository.retrieve_token_data.return_value = MOCK_GOOGLE_USER_DATA
        self.mock_user_repository.get_user_by_email.return_value = None

        with pytest.raises(AuthException):
            self.auth_service.get_user_login_data("auth_token")
