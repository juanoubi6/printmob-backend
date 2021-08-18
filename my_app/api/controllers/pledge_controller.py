import json
from typing import List

from flask import request

from my_app.api.domain import PledgePrototype, Pledge
from my_app.api.exceptions import BusinessException


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

    def update_pledge_with_payment(self, req: request, pledge_id: int):
        body = json.loads(req.data)
        payment_id = body["mp_payment_id"]

        updated_pledge = self.pledge_service.update_pledge_with_payment(pledge_id, payment_id)

        return updated_pledge.to_json(), 200

    def create_pledge_with_payment(self, req: request, user_data: dict):
        body = json.loads(req.data)
        campaign_id = body.get("campaign_id", None)
        payment_id = body.get("mp_payment_id", None)

        if campaign_id is None:
            raise BusinessException("Campaign information was not provided")

        if payment_id is None:
            raise BusinessException("Payment information was not provided")

        created_pledge = self.pledge_service.create_pledge_with_payment(
            campaign_id=int(campaign_id),
            payment_id=int(payment_id),
            buyer_id=int(user_data["id"])
        )

        return created_pledge.to_json(), 201
