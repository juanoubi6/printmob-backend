import unittest
from unittest.mock import Mock

from my_app.api.services import AuthService
from tests.utils.mock_entities import MOCK_GOOGLE_USER_DATA, MOCK_PRINTER_USER, MOCK_PRINTER, \
    MOCK_BUYER_USER, MOCK_BUYER

mock_google_repository = Mock()
mock_user_repository = Mock()
auth_service = AuthService(mock_google_repository, mock_user_repository)


class TestAuthService(unittest.TestCase):

    def setUp(self):
        mock_google_repository.reset_mock()
        mock_user_repository.reset_mock()

    def test_get_user_login_data_returns_printer_data_on_printer_login(self):
        mock_google_repository.retrieve_token_data.return_value = MOCK_GOOGLE_USER_DATA
        mock_user_repository.get_user_by_email.return_value = MOCK_PRINTER_USER
        mock_user_repository.get_printer_by_email.return_value = MOCK_PRINTER

        user, jwt = auth_service.get_user_login_data("auth_token")

        assert user == MOCK_PRINTER
        mock_google_repository.retrieve_token_data.assert_called_once_with("auth_token")
        mock_user_repository.get_user_by_email.assert_called_once_with(MOCK_GOOGLE_USER_DATA.email)
        mock_user_repository.get_printer_by_email.assert_called_once_with(MOCK_PRINTER_USER.email)

    def test_get_user_login_data_returns_buyer_data_on_buyer_login(self):
        mock_google_repository.retrieve_token_data.return_value = MOCK_GOOGLE_USER_DATA
        mock_user_repository.get_user_by_email.return_value = MOCK_BUYER_USER
        mock_user_repository.get_buyer_by_email.return_value = MOCK_BUYER

        user, jwt = auth_service.get_user_login_data("auth_token")

        assert user == MOCK_BUYER
        mock_google_repository.retrieve_token_data.assert_called_once_with("auth_token")
        mock_user_repository.get_user_by_email.assert_called_once_with(MOCK_GOOGLE_USER_DATA.email)
        mock_user_repository.get_buyer_by_email.assert_called_once_with(MOCK_BUYER_USER.email)
