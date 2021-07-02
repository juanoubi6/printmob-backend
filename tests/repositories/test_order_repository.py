import copy
import unittest
from unittest.mock import MagicMock

from my_app.api.domain import OrderStatus, Order
from my_app.api.repositories import OrderRepository
from tests.utils.mock_models import MOCK_ORDER_MODEL

test_db = MagicMock()
order_repository = OrderRepository(test_db)


class TestOrderRepository(unittest.TestCase):

    def setUp(self):
        test_db.reset_mock()

    def test_update_order_statuses_massively_returns_updated_orders(self):
        order_from_db = copy.deepcopy(MOCK_ORDER_MODEL)
        order_from_db.status = "In progress"

        test_db.session.query.return_value.filter.return_value.all.return_value = [order_from_db]

        response = order_repository.update_order_statuses_massively([1], OrderStatus.DISPATCHED)

        assert len(response) == 1
        assert isinstance(response[0], Order)
        assert response[0].status.value == OrderStatus.DISPATCHED.value
        test_db.session.commit.assert_called_once()
