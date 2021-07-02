from typing import List

from my_app.api.domain import OrderStatus, Order
from my_app.api.repositories.models import OrderModel


class OrderRepository:
    def __init__(self, db):
        self.db = db

    def update_order_statuses_massively(self, order_ids: List[int], new_status: OrderStatus) -> List[Order]:
        order_models = self.db.session.query(OrderModel) \
            .filter(OrderModel.id.in_(order_ids)) \
            .all()

        for order_model in order_models:
            order_model.status = new_status.value

        self.db.session.commit()

        return [order_model.to_order_entity() for order_model in order_models]
