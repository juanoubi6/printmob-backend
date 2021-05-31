from flask import request

from my_app.api.exceptions.BusinessException import BusinessException
from my_app.api.exceptions.NotFoundException import NotFoundException

CAMPAIGN_DETAIL_FAILED = 'Campaign detail retrieval has failed'


class CampaignController:
    def __init__(self, campaign_service):
        self.campaign_service = campaign_service

    def get_campaigns(self, req: request):
        campaigns = self.campaign_service.get_campaigns()

        return list(map(lambda c: c.to_json(), campaigns)), 200

    def get_campaign_detail(self, req: request, campaign_id):
        try:
            campaign = self.campaign_service.get_campaign_detail(campaign_id)
            return campaign.to_json(), 200
        except NotFoundException as nfe:
            raise nfe
        except Exception:
            raise BusinessException(CAMPAIGN_DETAIL_FAILED)
