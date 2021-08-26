import json
import os
import unittest
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.domain import Page
from my_app.api.utils.token_manager import TokenManager
from tests.test_utils.mock_entities import MOCK_ORDER, MOCK_PRINTER
from tests.test_utils.test_json import UPDATE_ORDER_STATUSES_MASSIVE_REQUEST_JSON, UPDATE_ORDER_REQUEST_JSON, \
    UPDATE_ORDER_RESPONSE_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestOrderController(unittest.TestCase):

    def setUp(self):
        token_manager = TokenManager(os.environ["JWT_SECRET_KEY"])
        self.printer_authorization_token = token_manager.get_token_from_payload(MOCK_PRINTER.identity_data())

    @patch.object(app.order_controller, "order_service")
    def test_update_order_statuses_massively_returns_ok(self, mock_order_service):
        mock_order_service.update_order_statuses_massively.return_value = None

        res = client.patch("/orders/status/massive", data=json.dumps(UPDATE_ORDER_STATUSES_MASSIVE_REQUEST_JSON))
        assert res.status_code == 200

    @patch.object(app.order_controller, "order_service")
    def test_update_order_returns_updated_order(self, mock_order_service):
        mock_order_service.update_order.return_value = MOCK_ORDER

        res = client.patch("/orders/1", data=json.dumps(UPDATE_ORDER_REQUEST_JSON))
        assert res.status_code == 200
        assert res.json == UPDATE_ORDER_RESPONSE_JSON

    @patch.object(app.order_controller, "order_service")
    def test_get_campaign_order_from_buyer_returns_order(self, mock_order_service):
        mock_order_service.get_campaign_order_from_buyer.return_value = MOCK_ORDER

        res = client.get("/orders/buyers/2/campaigns/1")
        assert res.status_code == 200
        assert res.json == UPDATE_ORDER_RESPONSE_JSON

    @patch.object(app.order_controller, "order_service")
    def test_get_orders_of_printer_returns_orders_page(self, mock_order_service):
        mock_order_service.get_orders_of_printer.return_value = Page(
            page=1,
            page_size=10,
            total_records=100,
            data=[MOCK_ORDER]
        )

        res = client.get(
            "/orders/printers/1?page=1&page_size=10",
            headers={"Authorization": self.printer_authorization_token}
        )

        assert res.status_code == 200
        assert res.json["page"] == 1
        assert res.json["page_size"] == 10
        assert res.json["total_records"] == 100
        assert res.json["data"][0]["id"] == MOCK_ORDER.id