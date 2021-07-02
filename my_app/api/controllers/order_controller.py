import json

from flask import request

from my_app.api.domain import OrderStatus, OrderPrototype, Order
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

    def update_order(self, req: request, order_id: int) -> (Order, int):
        body = json.loads(req.data)
        prototype = OrderPrototype(
            status=OrderStatus(body["status"]),
            mail_company=body["mail_company"],
            tracking_code=body["tracking_code"],
            comments=body["comments"]
        )

        updated_order = self.order_service.update_order(order_id, prototype)

        return updated_order.to_json(), 200
