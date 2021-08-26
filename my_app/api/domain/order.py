import enum
from typing import Optional

from my_app.api.domain.campaign import Campaign
from my_app.api.domain.buyer import Buyer


class OrderStatus(enum.Enum):
    IN_PROGRESS = "In progress"
    DISPATCHED = "Dispatched"


class Order:
    def __init__(
            self,
            id: int,
            campaign_id: int,
            campaign: Optional[Campaign],
            pledge_id: int,
            buyer: Buyer,
            status: OrderStatus,
            mail_company: str = None,
            tracking_code: str = None,
            comments: str = None
    ):
        self.id = id
        self.campaign = campaign
        self.campaign_id = campaign_id
        self.pledge_id = pledge_id
        self.buyer = buyer
        self.status = status
        self.mail_company = mail_company
        self.tracking_code = tracking_code
        self.comments = comments

    def get_translated_order_status(self):
        if self.status == OrderStatus.DISPATCHED:
            return "Despachada"
        elif self.status == OrderStatus.IN_PROGRESS:
            return "En progreso"
        else:
            return "Desconocido"

    def to_json(self):
        return {
            "id": self.id,
            "campaign": self.campaign.to_json() if self.campaign is not None else None,
            "buyer": self.buyer.to_json(),
            "status": self.status.value,
            "mail_company": self.mail_company,
            "tracking_code": self.tracking_code,
            "comments": self.comments
        }


class OrderPrototype:
    def __init__(
            self,
            status: OrderStatus,
            mail_company: str = None,
            tracking_code: str = None,
            comments: str = None
    ):
        self.status = status
        self.mail_company = mail_company
        self.tracking_code = tracking_code
        self.comments = comments
