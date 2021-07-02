import unittest
from unittest.mock import Mock

from my_app.api.domain import OrderStatus, OrderPrototype
from my_app.api.services import OrderService
from tests.utils.mock_entities import MOCK_ORDER

mock_order_repository = Mock()
mock_email_repository = Mock()
mock_executor = Mock()
order_service = OrderService(mock_order_repository, mock_email_repository, mock_executor)


class TestOrderService(unittest.TestCase):

    def setUp(self):
        mock_order_repository.reset_mock()
        mock_email_repository.reset_mock()
        mock_executor.reset_mock()

    def test_update_order_statuses_massively_executes_successfully(self):
        mock_order_repository.update_order_statuses_massively.return_value = [MOCK_ORDER]

        order_service.update_order_statuses_massively(
            order_ids=[MOCK_ORDER.id],
            new_status=OrderStatus.DISPATCHED
        )

        mock_order_repository.update_order_statuses_massively.assert_called_once_with(
            [MOCK_ORDER.id],
            OrderStatus.DISPATCHED
        )
        mock_executor.submit.assert_called_once()

    def test_update_order_returns_updated_order(self):
        mock_order_repository.update_order.return_value = MOCK_ORDER

        prototype = OrderPrototype(status=OrderStatus.DISPATCHED)
        order_service.update_order(
            order_id=MOCK_ORDER.id,
            prototype=prototype
        )

        mock_order_repository.update_order.assert_called_once_with(
            MOCK_ORDER.id,
            prototype
        )
        mock_executor.submit.assert_called_once()
