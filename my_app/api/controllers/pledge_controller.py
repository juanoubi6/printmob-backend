from flask import request


class PledgeController:
    def __init__(self, pledge_service):
        self.pledge_service = pledge_service

    def create_pledge(self, req: request):
        created_pledge = self.pledge_service.create_pledge(campaign_id)

        return created_pledge.to_json(), 201
