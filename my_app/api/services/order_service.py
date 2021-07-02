from concurrent.futures import Executor
from typing import List

from my_app.api.domain import OrderStatus
from my_app.api.repositories import EmailRepository, OrderRepository
from my_app.api.utils.email import create_updated_order_status_email_for_buyer


class OrderService:
    def __init__(
            self,
            order_repository: OrderRepository,
            email_repository: EmailRepository,
            executor: Executor
    ):
        self.order_repository = order_repository
        self.email_repository = email_repository
        self.executor = executor

    def update_order_statuses_massively(self, order_ids: List[int], new_status: OrderStatus):
        updated_orders = self.order_repository.update_order_statuses_massively(order_ids, new_status)

        buyer_emails = [
            create_updated_order_status_email_for_buyer(order.buyer.email, order) for order in updated_orders
        ]

        self.executor.submit(
            self.email_repository.send_many_emails_of_the_same_type,
            buyer_emails
        )
