import copy
import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import OrderStatus, Order, OrderPrototype, Printer, Buyer, User
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import OrderRepository, UserRepository
from tests.utils.mock_models import MOCK_ORDER_MODEL, MOCK_USER_PRINTER_MODEL, MOCK_PRINTER_MODEL, \
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
