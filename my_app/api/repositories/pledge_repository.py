from datetime import datetime

from my_app.api.domain import PledgePrototype, Pledge
from my_app.api.repositories.models import PledgeModel


class PledgeRepository:
    def __init__(self, db):
        self.db = db

    def create_pledge(self, prototype: PledgePrototype) -> Pledge:
        pledge_model = PledgeModel(campaign_id=prototype.campaign_id,
                                   pledge_price=prototype.pledge_price,
                                   buyer_id=prototype.buyer_id)
        self.db.session.add(pledge_model)
        self.db.session.commit()

        return pledge_model.to_pledge_entity()
