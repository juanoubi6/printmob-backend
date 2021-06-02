import datetime

from my_app.api.repositories.models import PledgeModel


class Pledge:
    def __init__(
            self,
            id: int,
            buyer_id: int,
            pledge_price: float,
            campaign_id: int,
            pledge_date: datetime.datetime
    ):
        self.id = id
        self.buyer_id = buyer_id
        self.pledge_price = pledge_price
        self.campaign_id = campaign_id
        self.pledge_date = pledge_date

    @staticmethod
    def from_model(pledge_model: PledgeModel):
        return Pledge(
            id=pledge_model.id,
            buyer_id=pledge_model.buyer_id,
            pledge_price=pledge_model.pledge_price,
            campaign_id=pledge_model.campaign_id,
            pledge_date=pledge_model.pledge_date,
        )

    def to_json(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "pledge_price": self.pledge_price,
            "campaign_id": self.campaign_id,
            "pledge_date": self.pledge_date
        }
