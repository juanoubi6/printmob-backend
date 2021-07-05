import copy
import unittest
from unittest.mock import MagicMock, patch

from my_app.api.domain import Printer, Buyer, User
from my_app.api.repositories import UserRepository
from tests.test_utils.mock_entities import MOCK_BUYER_PROTOTYPE
from tests.test_utils.mock_models import MOCK_USER_PRINTER_MODEL, MOCK_PRINTER_MODEL, \
    MOCK_USER_BUYER_MODEL, MOCK_BUYER_MODEL

test_db = MagicMock()
user_repository = UserRepository(test_db)


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        test_db.reset_mock()

    def test_get_printer_by_email_returns_printer(self):
        user_printer_model = copy.deepcopy(MOCK_USER_PRINTER_MODEL)
        user_printer_model.printer = MOCK_PRINTER_MODEL
        test_db.session.query.return_value.filter_by.return_value.first.return_value = user_printer_model

        response = user_repository.get_printer_by_email("email")

        assert isinstance(response, Printer)

    def test_get_buyer_by_email_returns_buyer(self):
        user_buyer_model = copy.deepcopy(MOCK_USER_BUYER_MODEL)
        user_buyer_model.buyer = MOCK_BUYER_MODEL
        test_db.session.query.return_value.filter_by.return_value.first.return_value = user_buyer_model

        response = user_repository.get_buyer_by_email("email")

        assert isinstance(response, Buyer)

    def test_get_user_by_email_returns_user(self):
        test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = user_repository.get_user_by_email("email")

        assert isinstance(response, User)

    def test_is_user_name_in_use_returns_true_if_user_name_is_being_used(self):
        test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = user_repository.is_user_name_in_use("username")

        assert response is True

    def test_is_email_in_use_returns_true_if_email_is_being_used(self):
        test_db.session.query.return_value.filter_by.return_value.first.return_value = MOCK_USER_BUYER_MODEL

        response = user_repository.is_email_in_use("email")

        assert response is True

    @patch('my_app.api.repositories.user_repository.BuyerModel')
    def test_create_buyer_creates_buyer(self, mock_buyer_model_instance):
        mock_buyer_model_instance.return_value = MOCK_BUYER_MODEL

        response = user_repository.create_buyer(MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Buyer)
        assert test_db.session.add.call_count == 3
        test_db.session.flush.assert_called_once()
        test_db.session.commit.assert_called_once()

    @patch('my_app.api.repositories.user_repository.PrinterModel')
    def test_create_printer_creates_buyer(self, mock_printer_model_instance):
        mock_printer_model_instance.return_value = MOCK_PRINTER_MODEL

        response = user_repository.create_printer(MOCK_BUYER_PROTOTYPE)

        assert isinstance(response, Printer)
        assert test_db.session.add.call_count == 2
        test_db.session.flush.assert_called_once()
        test_db.session.commit.assert_called_once()
