from concurrent.futures import Executor
from typing import List

from my_app.api.domain import OrderStatus, OrderPrototype, Order
from my_app.api.repositories import EmailRepository, OrderRepository, CampaignRepository
from my_app.api.utils.email import create_updated_order_status_email_for_buyer, create_updated_order_email_for_buyer


class OrderService:
    def __init__(
            self,
            order_repository: OrderRepository,
            campaign_repository: CampaignRepository,
            email_repository: EmailRepository,
            executor: Executor
    ):
        self.order_repository = order_repository
        self.campaign_repository = campaign_repository
        self.email_repository = email_repository
        self.executor = executor

    def update_order_statuses_massively(self, order_ids: List[int], new_status: OrderStatus):
        if len(order_ids) > 0:
            updated_orders = self.order_repository.update_order_statuses_massively(order_ids, new_status)
            campaign = self.campaign_repository.get_campaign_detail(updated_orders[0].campaign_id)

            buyer_emails = [
                create_updated_order_status_email_for_buyer(order.buyer.email, campaign, order) for order in updated_orders
            ]

            self.executor.submit(
                self.email_repository.send_many_emails_of_the_same_type,
                buyer_emails
            )

    def update_order(self, order_id: int, prototype: OrderPrototype) -> Order:
        updated_order = self.order_repository.update_order(order_id, prototype)
        campaign = self.campaign_repository.get_campaign_detail(updated_order.campaign_id)

        self.executor.submit(
            self.email_repository.send_individual_email,
            create_updated_order_email_for_buyer(updated_order.buyer.email, campaign)
        )

        return updated_order

    def get_campaign_order_from_buyer(self, buyer_id: int, campaign_id: int) -> Order:
        return self.order_repository.get_campaign_order_from_buyer(buyer_id, campaign_id)
