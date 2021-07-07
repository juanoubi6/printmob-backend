import copy
import unittest
from unittest.mock import MagicMock

import pytest

from my_app.api.domain import OrderStatus, Order, OrderPrototype
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import OrderRepository
from tests.test_utils.mock_models import MOCK_ORDER_MODEL

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

    def test_update_order_returns_updated_order(self):
        order_from_db = copy.deepcopy(MOCK_ORDER_MODEL)
        order_from_db.status = "In progress"
        order_from_db.mail_company = None
        order_from_db.tracking_code = None
        order_from_db.comments = None

        prototype = OrderPrototype(
            status=OrderStatus.DISPATCHED,
            mail_company="OCA",
            tracking_code="1234",
            comments="comment"
        )

        test_db.session.query.return_value.filter_by.return_value.first.return_value = order_from_db

        response = order_repository.update_order(1, prototype)

        assert isinstance(response, Order)
        assert response.status.value == OrderStatus.DISPATCHED.value
        assert response.mail_company == prototype.mail_company
        assert response.tracking_code == prototype.tracking_code
        assert response.comments == prototype.comments
        test_db.session.commit.assert_called_once()

    def test_update_order_throws_exception_when_order_cannot_be_found(self):
        prototype = OrderPrototype(status=OrderStatus.DISPATCHED)

        test_db.session.query.return_value.filter_by.return_value.first.return_value = None

        with pytest.raises(NotFoundException):
            order_repository.update_order(1, prototype)