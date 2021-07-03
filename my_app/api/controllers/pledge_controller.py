import json
from typing import List

from flask import request

from my_app.api.domain import PledgePrototype, Pledge


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

    def cancel_pledge(self, req: request, pledge_id: int) -> (dict, int):
        self.pledge_service.cancel_pledge(pledge_id)

        return {"status": "ok"}, 200

    def get_pledges(self, req: request) -> (List[Pledge], int):
        filters = req.args
        pledges = self.pledge_service.get_pledges(filters)

        return [pledge.to_json() for pledge in pledges], 200
