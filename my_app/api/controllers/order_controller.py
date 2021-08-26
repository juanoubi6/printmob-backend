import json

from flask import request

from my_app.api.controllers.validators import validate_pagination_filters
from my_app.api.domain import OrderStatus, OrderPrototype, Order, Page
from my_app.api.exceptions import BusinessException
from my_app.api.services import OrderService

USER_MISMATCH_ERROR = "Tu usuario no tiene permisos para acceder a esta información"


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

    def get_campaign_order_from_buyer(self, req: request, buyer_id: int, campaign_id: int) -> (Order, int):
        order = self.order_service.get_campaign_order_from_buyer(buyer_id, campaign_id)

        return order.to_json(), 200

    def get_orders_of_printer(self, req: request, printer_id:int, user_data:dict) -> (Page[Order], int):
        if printer_id != int(user_data["id"]):
            return BusinessException(USER_MISMATCH_ERROR)

        filters = req.args
        validate_pagination_filters(filters)
        orders_page = self.order_service.get_orders_of_printer(printer_id, filters)

        return orders_page.to_json(), 200
