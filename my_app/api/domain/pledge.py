import datetime


class Pledge:
    def __init__(
            self,
            id: int,
            buyer_id: int,
            pledge_price: float,
            campaign_id: int,
            created_at: datetime.datetime = datetime.datetime.utcnow(),
            updated_at: datetime.datetime = datetime.datetime.utcnow(),
            deleted_at: datetime.datetime = None
    ):
        self.id = id
        self.buyer_id = buyer_id
        self.pledge_price = pledge_price
        self.campaign_id = campaign_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_json(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "pledge_price": self.pledge_price,
            "campaign_id": self.campaign_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
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
