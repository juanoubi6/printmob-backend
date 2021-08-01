import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import Printer, Buyer
from my_app.api.exceptions import BusinessException
from my_app.api.services import UserService
from tests.test_utils.mock_entities import MOCK_PRINTER, MOCK_PRINTER_PROTOTYPE, MOCK_BUYER, MOCK_BUYER_PROTOTYPE


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.mock_user_repository = MagicMock()
        self.user_service = UserService(self.mock_user_repository)

    def test_create_printer_returns_printer(self):
        self.mock_user_repository.is_user_name_in_use.return_value = False
        self.mock_user_repository.is_email_in_use.return_value = False
        self.mock_user_repository.create_printer.return_value = MOCK_PRINTER

        response = self.user_service.create_printer(MOCK_PRINTER_PROTOTYPE)

        assert isinstance(response, Printer)
        self.mock_user_repository.is_user_name_in_use.assert_called_once()
        self.mock_user_repository.is_email_in_use.assert_called_once()
        self.mock_user_repository.create_printer.assert_called_once_with(MOCK_PRINTER_PROTOTYPE)

    def test_create_printer_raises_error_when_user_name_already_in_use(self):
        self.mock_user_repository.is_user_name_in_use.return_value = True

        with pytest.raises(BusinessException):
            self.user_service.create_printer(MOCK_PRINTER_PROTOTYPE)

    def test_create_printer_raises_error_when_email_already_in_use(self):
        self.mock_user_repository.is_user_name_in_use.return_value = False
        self.mock_user_repository.is_email_in_use.return_value = True

        with pytest.raises(BusinessException):
            self.user_service.create_printer(MOCK_PRINTER_PROTOTYPE)

    def test_create_buyer_returns_buyer(self):
        self.mock_user_repository.is_user_name_in_use.return_value = False
        self.mock_user_repository.is_email_in_use.return_value = False
        self.mock_user_repository.create_buyer.return_value = MOCK_BUYER

        response = self.user_service.create_buyer(MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Buyer)
        self.mock_user_repository.is_user_name_in_use.assert_called_once()
        self.mock_user_repository.is_email_in_use.assert_called_once()
        self.mock_user_repository.create_buyer.assert_called_once_with(MOCK_BUYER_PROTOTYPE)

    def test_create_buyer_raises_error_when_user_name_already_in_use(self):
        self.mock_user_repository.is_user_name_in_use.return_value = True

        with pytest.raises(BusinessException):
            self.user_service.create_buyer(MOCK_BUYER_PROTOTYPE)

    def test_create_buyer_raises_error_when_email_already_in_use(self):
        self.mock_user_repository.is_user_name_in_use.return_value = False
        self.mock_user_repository.is_email_in_use.return_value = True

        with pytest.raises(BusinessException):
            self.user_service.create_buyer(MOCK_BUYER_PROTOTYPE)

    def test_get_printer_by_email_returns_printer(self):
        self.mock_user_repository.get_printer_by_email.return_value = MOCK_PRINTER

        response = self.user_service.get_printer_by_email(MOCK_PRINTER.email)

        assert isinstance(response, Printer)
        self.mock_user_repository.get_printer_by_email.assert_called_once_with(MOCK_PRINTER.email)

    def test_get_buyer_by_email_returns_printer(self):
        self.mock_user_repository.get_buyer_by_email.return_value = MOCK_BUYER

        response = self.user_service.get_buyer_by_email(MOCK_BUYER.email)

        assert isinstance(response, Buyer)
        self.mock_user_repository.get_buyer_by_email.assert_called_once_with(MOCK_BUYER.email)

    def test_update_printer_returns_printer(self):
        self.mock_user_repository.update_printer.return_value = MOCK_PRINTER

        response = self.user_service.update_printer(1, MOCK_PRINTER_PROTOTYPE)

        assert isinstance(response, Printer)
        self.mock_user_repository.update_printer.assert_called_once_with(1, MOCK_PRINTER_PROTOTYPE)

    def test_update_buyer_returns_printer(self):
        self.mock_user_repository.update_buyer.return_value = MOCK_BUYER

        response = self.user_service.update_buyer(1, MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Buyer)
        self.mock_user_repository.update_buyer.assert_called_once_with(1, MOCK_BUYER_PROTOTYPE)

    def test_validate_user_name_and_email_existence_returns_validation(self):
        self.mock_user_repository.is_email_in_use.return_value = True
        self.mock_user_repository.is_user_name_in_use.return_value = False

        response = self.user_service.validate_user_name_and_email_existence("user_name", "email")

        assert response["email"] is True
        assert response["user_name"] is False

        self.mock_user_repository.is_email_in_use.assert_called_once_with("email")
        self.mock_user_repository.is_user_name_in_use.assert_called_once_with("user_name")
