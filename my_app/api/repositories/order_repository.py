from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import lazyload, noload

from my_app.api.domain import OrderStatus, Order, OrderPrototype, Page
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories.models import OrderModel, CampaignModel
from my_app.api.repositories.utils import apply_campaign_order_filters, paginate, DEFAULT_PAGE, DEFAULT_PAGE_SIZE

ORDER_NOT_FOUND = "La orden no existe"


class OrderRepository:
    def __init__(self, db):
        self.db = db

    def update_order_statuses_massively(self, order_ids: List[int], new_status: OrderStatus) -> List[Order]:
        order_models = self.db.session.query(OrderModel) \
            .filter(OrderModel.id.in_(order_ids)) \
            .options(noload(OrderModel.campaign)) \
            .all()

        for order_model in order_models:
            order_model.status = new_status.value

        self.db.session.commit()

        return [order_model.to_order_entity() for order_model in order_models]

    def update_order(self, order_id: int, prototype: OrderPrototype) -> Order:
        order_model = self.db.session.query(OrderModel) \
            .filter_by(id=order_id) \
            .options(noload(OrderModel.campaign)) \
            .first()

        if order_model is None:
            raise NotFoundException(ORDER_NOT_FOUND)

        order_model.status = prototype.status.value
        order_model.mail_company = prototype.mail_company
        order_model.tracking_code = prototype.tracking_code
        order_model.comments = prototype.comments

        self.db.session.commit()

        return order_model.to_order_entity()

    def get_campaign_order_from_buyer(self, buyer_id: int, campaign_id: int) -> Order:
        order_model = self.db.session.query(OrderModel) \
            .filter(OrderModel.buyer_id == buyer_id) \
            .filter(OrderModel.campaign_id == campaign_id) \
            .first()

        if order_model is None:
            raise NotFoundException(ORDER_NOT_FOUND)

        return order_model.to_order_entity()

    def get_orders_of_printer(self, printer_id: int, filters: dict) -> Page[Order]:
        query = self.db.session.query(OrderModel).join(CampaignModel, OrderModel.campaign_id == CampaignModel.id)
        query = query.filter(CampaignModel.printer_id == printer_id)
        query = apply_campaign_order_filters(query, filters)
        query = query.options(lazyload(OrderModel.campaign).options(
            noload(CampaignModel.printer),
            noload(CampaignModel.tech_detail),
            noload(CampaignModel.pledges),
            noload(CampaignModel.images)
        ))
        query = query.order_by(asc(OrderModel.id))

        order_models = paginate(query, filters).all()
        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=[om.to_order_entity() for om in order_models]
        )
