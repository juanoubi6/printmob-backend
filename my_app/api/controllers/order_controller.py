import json

from flask import request

from my_app.api.domain import OrderStatus
from my_app.api.services import OrderService


class OrderController:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def update_order_statuses_massively(self, req: request) -> (dict, int):
        body = json.loads(req.data)
        order_ids = body["order_ids"]
        new_status = OrderStatus(body["status"])

        self.order_service.update_order_statuses_massively(order_ids, new_status)

        return {"status": "ok"}, 200
