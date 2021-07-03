import enum

from my_app.api.domain import Buyer


class OrderStatus(enum.Enum):
    IN_PROGRESS = "In progress"
    DISPATCHED = "Dispatched"


class Order:
    def __init__(
            self,
            id: int,
            campaign_id: int,
            pledge_id: int,
            buyer: Buyer,
            status: OrderStatus,
            mail_company: str = None,
            tracking_code: str = None,
            comments: str = None
    ):
        self.id = id
        self.campaign_id = campaign_id
        self.pledge_id = pledge_id
        self.buyer = buyer
        self.status = status
        self.mail_company = mail_company
        self.tracking_code = tracking_code
        self.comments = comments

    def to_json(self):
        return {
            "id": self.id,
            "buyer": self.buyer.to_json(),
            "status": self.status.value,
            "mail_company": self.mail_company,
            "tracking_code": self.tracking_code,
            "comments": self.comments
        }
