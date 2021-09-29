import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import Printer, Buyer, Balance, Designer, PrinterDataDashboard, DesignerDataDashboard, \
    BuyerDataDashboard
from my_app.api.exceptions import BusinessException
from my_app.api.services import UserService
from tests.test_utils.mock_entities import MOCK_PRINTER, MOCK_PRINTER_PROTOTYPE, MOCK_BUYER, MOCK_BUYER_PROTOTYPE, \
    MOCK_BALANCE, MOCK_DESIGNER, MOCK_DESIGNER_PROTOTYPE, MOCK_PRINTER_DATA_DASHBOARD, MOCK_DESIGNER_DATA_DASHBOARD, \
    MOCK_BUYER_DATA_DASHBOARD


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.mock_transaction_repository = MagicMock()
        self.mock_user_repository = MagicMock()
        self.mock_email_repository = MagicMock()
        self.mock_executor = MagicMock()
        self.user_service = UserService(self.mock_user_repository, self.mock_transaction_repository,
                                        self.mock_email_repository, self.mock_executor)

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

    def test_create_designer_returns_designer(self):
        self.mock_user_repository.is_user_name_in_use.return_value = False
        self.mock_user_repository.is_email_in_use.return_value = False
        self.mock_user_repository.create_designer.return_value = MOCK_DESIGNER

        response = self.user_service.create_designer(MOCK_DESIGNER_PROTOTYPE)

        assert isinstance(response, Designer)
        self.mock_user_repository.is_user_name_in_use.assert_called_once()
        self.mock_user_repository.is_email_in_use.assert_called_once()
        self.mock_user_repository.create_designer.assert_called_once_with(MOCK_DESIGNER_PROTOTYPE)

    def test_create_designer_raises_error_when_user_name_already_in_use(self):
        self.mock_user_repository.is_user_name_in_use.return_value = True

        with pytest.raises(BusinessException):
            self.user_service.create_designer(MOCK_DESIGNER_PROTOTYPE)

    def test_create_designer_raises_error_when_email_already_in_use(self):
        self.mock_user_repository.is_user_name_in_use.return_value = False
        self.mock_user_repository.is_email_in_use.return_value = True

        with pytest.raises(BusinessException):
            self.user_service.create_designer(MOCK_DESIGNER_PROTOTYPE)

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

    def test_get_designer_by_email_returns_printer(self):
        self.mock_user_repository.get_designer_by_email.return_value = MOCK_DESIGNER

        response = self.user_service.get_designer_by_email(MOCK_DESIGNER.email)

        assert isinstance(response, Designer)
        self.mock_user_repository.get_designer_by_email.assert_called_once_with(MOCK_DESIGNER.email)


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

    def test_update_designer_returns_printer(self):
        self.mock_user_repository.update_designer.return_value = MOCK_DESIGNER

        response = self.user_service.update_designer(1, MOCK_DESIGNER_PROTOTYPE)

        assert isinstance(response, Designer)
        self.mock_user_repository.update_designer.assert_called_once_with(1, MOCK_DESIGNER_PROTOTYPE)


    def test_update_buyer_returns_printer(self):
        self.mock_user_repository.update_buyer.return_value = MOCK_BUYER

        response = self.user_service.update_buyer(1, MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Buyer)
        self.mock_user_repository.update_buyer.assert_called_once_with(1, MOCK_BUYER_PROTOTYPE)

    def test_get_user_balance_returns_balance(self):
        self.mock_transaction_repository.get_user_balance.return_value = MOCK_BALANCE

        response = self.user_service.get_user_balance(1)

        assert isinstance(response, Balance)
        self.mock_transaction_repository.get_user_balance.assert_called_once_with(1)

    def test_request_user_balance_sends_email_if_balance_is_not_0_and_send_notification_flag_is_true(self):
        self.mock_transaction_repository.create_balance_request.return_value = (50.0, True)
        self.mock_user_repository.get_user_by_id.return_value = MOCK_PRINTER

        self.user_service.request_balance(MOCK_PRINTER.id)

        self.mock_executor.submit.assert_called_once()

    def test_request_user_balance_does_not_send_email_if_balance_is_0(self):
        self.mock_transaction_repository.create_balance_request.return_value = (0.0, True)
        self.mock_user_repository.get_user_by_id.return_value = MOCK_PRINTER

        self.user_service.request_balance(MOCK_PRINTER.id)

        self.mock_executor.submit.assert_not_called()

    def test_validate_user_name_and_email_existence_returns_validation(self):
        self.mock_user_repository.is_email_in_use.return_value = True
        self.mock_user_repository.is_user_name_in_use.return_value = False

        response = self.user_service.validate_user_name_and_email_existence("user_name", "email")

        assert response["email"] is True
        assert response["user_name"] is False

        self.mock_user_repository.is_email_in_use.assert_called_once_with("email")
        self.mock_user_repository.is_user_name_in_use.assert_called_once_with("user_name")

    def test_get_printer_data_dashboard_returns_printer_data_dashboard(self):
        self.mock_user_repository.get_printer_data_dashboard.return_value = MOCK_PRINTER_DATA_DASHBOARD

        response = self.user_service.get_printer_data_dashboard(MOCK_PRINTER.id)

        assert isinstance(response, PrinterDataDashboard)
        self.mock_user_repository.get_printer_data_dashboard.assert_called_once_with(MOCK_PRINTER.id)

    def test_get_designer_data_dashboard_returns_designer_data_dashboard(self):
        self.mock_user_repository.get_designer_data_dashboard.return_value = MOCK_DESIGNER_DATA_DASHBOARD

        response = self.user_service.get_designer_data_dashboard(MOCK_DESIGNER.id)

        assert isinstance(response, DesignerDataDashboard)
        self.mock_user_repository.get_designer_data_dashboard.assert_called_once_with(MOCK_DESIGNER.id)

    def test_get_buyer_data_dashboard_returns_buyer_data_dashboard(self):
        self.mock_user_repository.get_buyer_data_dashboard.return_value = MOCK_BUYER_DATA_DASHBOARD

        response = self.user_service.get_buyer_data_dashboard(MOCK_BUYER.id)

        assert isinstance(response, BuyerDataDashboard)
        self.mock_user_repository.get_buyer_data_dashboard.assert_called_once_with(MOCK_BUYER.id)
