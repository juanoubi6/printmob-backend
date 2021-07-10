import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import Printer, Buyer
from my_app.api.exceptions import BusinessException
from my_app.api.services import UserService
from tests.test_utils.mock_entities import MOCK_PRINTER, MOCK_PRINTER_PROTOTYPE, MOCK_BUYER, MOCK_BUYER_PROTOTYPE

mock_user_repository = MagicMock()
user_service = UserService(mock_user_repository)


class TestUserService(unittest.TestCase):

    def setUp(self):
        mock_user_repository.reset_mock()

    def test_create_printer_returns_printer(self):
        mock_user_repository.is_user_name_in_use.return_value = False
        mock_user_repository.is_email_in_use.return_value = False
        mock_user_repository.create_printer.return_value = MOCK_PRINTER

        response = user_service.create_printer(MOCK_PRINTER_PROTOTYPE)

        assert isinstance(response, Printer)
        mock_user_repository.is_user_name_in_use.assert_called_once()
        mock_user_repository.is_email_in_use.assert_called_once()
        mock_user_repository.create_printer.assert_called_once_with(MOCK_PRINTER_PROTOTYPE)

    def test_create_printer_raises_error_when_user_name_already_in_use(self):
        mock_user_repository.is_user_name_in_use.return_value = True

        with pytest.raises(BusinessException):
            user_service.create_printer(MOCK_PRINTER_PROTOTYPE)

    def test_create_printer_raises_error_when_email_already_in_use(self):
        mock_user_repository.is_user_name_in_use.return_value = False
        mock_user_repository.is_email_in_use.return_value = True

        with pytest.raises(BusinessException):
            user_service.create_printer(MOCK_PRINTER_PROTOTYPE)

    def test_create_buyer_returns_buyer(self):
        mock_user_repository.is_user_name_in_use.return_value = False
        mock_user_repository.is_email_in_use.return_value = False
        mock_user_repository.create_buyer.return_value = MOCK_BUYER

        response = user_service.create_buyer(MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Buyer)
        mock_user_repository.is_user_name_in_use.assert_called_once()
        mock_user_repository.is_email_in_use.assert_called_once()
        mock_user_repository.create_buyer.assert_called_once_with(MOCK_BUYER_PROTOTYPE)

    def test_create_buyer_raises_error_when_user_name_already_in_use(self):
        mock_user_repository.is_user_name_in_use.return_value = True

        with pytest.raises(BusinessException):
            user_service.create_buyer(MOCK_BUYER_PROTOTYPE)

    def test_create_buyer_raises_error_when_email_already_in_use(self):
        mock_user_repository.is_user_name_in_use.return_value = False
        mock_user_repository.is_email_in_use.return_value = True

        with pytest.raises(BusinessException):
            user_service.create_buyer(MOCK_BUYER_PROTOTYPE)
