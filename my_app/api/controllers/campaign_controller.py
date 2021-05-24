from flask import request


class CampaignController:
    def __init__(self, campaign_service):
        self.campaign_service = campaign_service

    def get_campaigns(self, req: request):
        campaigns = self.campaign_service.get_campaigns()

        return list(map(lambda c: c.to_json(), campaigns)), 200
