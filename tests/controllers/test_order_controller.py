import json
import unittest
from unittest.mock import patch

from my_app.api import create_app
from tests.utils.mock_entities import MOCK_ORDER
from tests.utils.test_json import UPDATE_ORDER_STATUSES_MASSIVE_REQUEST_JSON, UPDATE_ORDER_REQUEST_JSON, \
    UPDATE_ORDER_RESPONSE_JSON

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


class TestOrderController(unittest.TestCase):

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
