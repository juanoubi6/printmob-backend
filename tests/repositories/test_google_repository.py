import copy
import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import OrderStatus, Order, OrderPrototype, Printer, Buyer, User
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import OrderRepository, UserRepository, GoogleRepository
from tests.utils.mock_models import MOCK_ORDER_MODEL, MOCK_USER_PRINTER_MODEL, MOCK_PRINTER_MODEL, \
    MOCK_USER_BUYER_MODEL, MOCK_BUYER_MODEL

client_id = "mock_client_id"
google_fallback_url = "mock_fallback_url"
google_repository = GoogleRepository(client_id, google_fallback_url)


class TestUserRepository(unittest.TestCase):

    def test_retrieve_token_data_returns_google_user_data_on_default_flow_success(self):
        pass

    def test_retrieve_token_data_returns_google_user_data_using_fallback_flow(self):
        pass

    def test_retrieve_token_data_raises_exception_if_default_flow_fails(self):
        pass

    def test_retrieve_token_data_raises_exception_if_fallback_flow_fails_to_validate_token(self):
        pass