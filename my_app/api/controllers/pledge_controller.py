import json
from typing import List

from flask import request

from my_app.api.domain import Pledge
from my_app.api.exceptions import BusinessException


class PledgeController:
    def __init__(self, pledge_service):
        self.pledge_service = pledge_service

    def cancel_pledge(self, req: request, pledge_id: int) -> (dict, int):
        self.pledge_service.cancel_pledge(pledge_id)

        return {"status": "ok"}, 200

    def get_pledges(self, req: request) -> (List[Pledge], int):
        filters = req.args
        pledges = self.pledge_service.get_pledges(filters)

        return [pledge.to_json() for pledge in pledges], 200

    def create_pledge_with_payment(self, req: request, user_data: dict):
        body = json.loads(req.data)
        campaign_id = body.get("campaign_id", None)
        payment_id = body.get("mp_payment_id", None)

        if campaign_id is None:
            raise BusinessException("El ID de la campaña no fue provisto")

        if payment_id is None:
            raise BusinessException("El ID del pago no fue provisto")

        created_pledge = self.pledge_service.create_pledge_with_payment(
            campaign_id=int(campaign_id),
            payment_id=int(payment_id),
            buyer_id=int(user_data["id"])
        )

        return created_pledge.to_json(), 201
