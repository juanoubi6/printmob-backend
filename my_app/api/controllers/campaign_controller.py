from flask import request

from my_app.api.controllers.validators import validate_pagination_filters
from my_app.api.domain import Page, Campaign

CAMPAIGN_DETAIL_FAILED = 'Campaign detail retrieval has failed'


class CampaignController:
    def __init__(self, campaign_service):
        self.campaign_service = campaign_service

    def get_campaigns(self, req: request) -> (Page[Campaign], int):
        filters = req.args
        validate_pagination_filters(filters)
        campaigns_page = self.campaign_service.get_campaigns(filters)

        return campaigns_page.to_json(), 200

    def get_campaign_detail(self, req: request, campaign_id) -> (Campaign, int):
        campaign = self.campaign_service.get_campaign_detail(campaign_id)

        return campaign.to_json(), 200
