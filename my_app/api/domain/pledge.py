import datetime


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

    def to_json(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "pledge_price": self.pledge_price,
            "campaign_id": self.campaign_id,
            "pledge_date": self.pledge_date
        }


class PledgePrototype:
    def __init__(
            self,
            buyer_id: int,
            pledge_price: float,
            campaign_id: int,
    ):
        self.buyer_id = buyer_id
        self.pledge_price = pledge_price
        self.campaign_id = campaign_id
