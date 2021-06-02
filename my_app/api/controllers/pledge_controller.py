import json

from flask import request

from my_app.api.domain import PledgePrototype


class PledgeController:
    def __init__(self, pledge_service):
        self.pledge_service = pledge_service

    def create_pledge(self, req: request):
        body = json.loads(req.data)
        prototype = PledgePrototype(
            pledge_price=body["pledge_price"],
            campaign_id=body["campaign_id"],
            buyer_id=body["buyer_id"]
        )
        created_pledge = self.pledge_service.create_pledge(prototype)

        return created_pledge.to_json(), 201
