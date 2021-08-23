import unittest
from unittest.mock import MagicMock

from my_app.api.repositories import TransactionRepository


class TestTransactionRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = MagicMock()
        self.transaction_repository = TransactionRepository(self.test_db)

    def test_get_user_balance_returns_balance_when_data_is_found(self):
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (800,)

        result = self.transaction_repository.get_user_balance(1)

        assert result.future_balance == 800
        assert result.current_balance == 800

    def test_get_user_balance_returns_balance_as_zero_when_data_is_not_found(self):
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (None,)

        result = self.transaction_repository.get_user_balance(1)

        assert result.future_balance == 0
        assert result.current_balance == 0

    def test_create_balance_request_does_not_create_balance_request_is_current_balance_is_0(self):
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (0.0,)

        result = self.transaction_repository.create_balance_request(1)

        assert result == 0
        self.test_db.session.commit.assert_not_called()

    def test_create_balance_request_does_create_balance_request_is_current_balance_is_not_0(self):
        self.test_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (50,)

        result = self.transaction_repository.create_balance_request(1)

        assert result == 50
        self.test_db.session.commit.assert_called_once()
