import datetime
import unittest
from unittest.mock import MagicMock, Mock

import pytest

from my_app.api.domain import Pledge
from my_app.api.exceptions import BusinessException
from my_app.api.repositories import TransactionRepository
from my_app.api.repositories.models import PledgeModel
from tests.test_utils.mock_entities import MOCK_TRANSACTION_PROTOTYPE, MOCK_CAMPAIGN


class TestTransactionRepository(unittest.TestCase):

    def setUp(self):
        self.test_db = MagicMock()
        self.mock_pledge_repository = Mock()
        self.transaction_repository = TransactionRepository(self.test_db, self.mock_pledge_repository)

    def test_associate_transactions_to_pledge_returns_updated_pledge(self):
        pledge_to_update = PledgeModel(
            id=1,
            campaign_id=1,
            pledge_price=1.1,
            buyer_id=1,
            buyer=None,
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17)
        )
        self.mock_pledge_repository.get_pledge_model_by_id.return_value = pledge_to_update
        self.mock_pledge_repository.get_pledge_campaign.return_value = MOCK_CAMPAIGN

        response = self.transaction_repository.associate_transactions_to_pledge(1, MOCK_TRANSACTION_PROTOTYPE)

        assert isinstance(response, Pledge)
        self.test_db.session.commit.assert_called_once()

    def test_associate_transactions_rollbacks_transaction_creation_and_deletes_pledge_on_failure(self):
        pledge_to_update = PledgeModel(
            id=1,
            campaign_id=1,
            pledge_price=1.1,
            buyer_id=1,
            buyer=None,
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17),
            deleted_at=None
        )
        self.mock_pledge_repository.get_pledge_model_by_id.return_value = pledge_to_update
        self.mock_pledge_repository.get_pledge_campaign.return_value = MOCK_CAMPAIGN

        self.test_db.session.flush.side_effect = Exception("Some error")

        with pytest.raises(BusinessException):
            self.transaction_repository.associate_transactions_to_pledge(1, MOCK_TRANSACTION_PROTOTYPE)

        self.test_db.session.rollback.assert_called_once()
        self.test_db.session.commit.assert_called_once()
        assert pledge_to_update.deleted_at is not None

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
