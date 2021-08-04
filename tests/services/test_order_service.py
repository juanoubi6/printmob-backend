import unittest
from unittest.mock import Mock

from my_app.api.domain import OrderStatus, OrderPrototype, Order
from my_app.api.services import OrderService
from tests.test_utils.mock_entities import MOCK_ORDER


class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.mock_order_repository = Mock()
        self.mock_email_repository = Mock()
        self.mock_executor = Mock()
        self.order_service = OrderService(self.mock_order_repository, self.mock_email_repository, self.mock_executor)

    def test_update_order_statuses_massively_executes_successfully(self):
        self.mock_order_repository.update_order_statuses_massively.return_value = [MOCK_ORDER]

        self.order_service.update_order_statuses_massively(
            order_ids=[MOCK_ORDER.id],
            new_status=OrderStatus.DISPATCHED
        )

        self.mock_order_repository.update_order_statuses_massively.assert_called_once_with(
            [MOCK_ORDER.id],
            OrderStatus.DISPATCHED
        )
        self.mock_executor.submit.assert_called_once()

    def test_update_order_returns_updated_order(self):
        self.mock_order_repository.update_order.return_value = MOCK_ORDER

        prototype = OrderPrototype(status=OrderStatus.DISPATCHED)
        self.order_service.update_order(
            order_id=MOCK_ORDER.id,
            prototype=prototype
        )

        self.mock_order_repository.update_order.assert_called_once_with(
            MOCK_ORDER.id,
            prototype
        )
        self.mock_executor.submit.assert_called_once()

    def test_get_campaign_order_from_buyer_returns_order(self):
        self.mock_order_repository.get_campaign_order_from_buyer.return_value = MOCK_ORDER

        response = self.order_service.get_campaign_order_from_buyer(1, 2)

        assert isinstance(response, Order)
        self.mock_order_repository.get_campaign_order_from_buyer.assert_called_once_with(1, 2)
