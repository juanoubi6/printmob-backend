import json
from datetime import datetime

from flask import request

from my_app.api.controllers.validators import validate_pagination_filters, validate_campaign_prototype
from my_app.api.domain import Page, Campaign, CampaignModelImage
from my_app.api.domain.campaign import CampaignPrototype
from my_app.api.domain.tech_detail import TechDetailPrototype

CAMPAIGN_DETAIL_FAILED = 'Campaign detail retrieval has failed'


class CampaignController:
    def __init__(self, campaign_service):
        self.campaign_service = campaign_service

    def post_campaign(self, req: request) -> (Campaign, int):
        body = json.loads(req.data)
        prototype = CampaignPrototype(
            name=body["name"],
            description=body["description"],
            campaign_picture_url=None,
            campaign_model_image_urls=[],
            printer_id=body["printer_id"],
            pledge_price=body["pledge_price"],
            start_date=datetime.strptime(body["start_date"], '%d-%m-%Y %H:%M:%S'),
            end_date=datetime.strptime(body["end_date"], '%d-%m-%Y %H:%M:%S'),
            min_pledgers=body["min_pledgers"],
            max_pledgers=body["max_pledgers"],
            tech_details=TechDetailPrototype(
                material=body["tech_details"]["material"],
                weight=body["tech_details"]["weight"],
                width=body["tech_details"]["width"],
                length=body["tech_details"]["length"],
                depth=body["tech_details"]["depth"],
            )
        )
        validate_campaign_prototype(prototype)
        created_campaign = self.campaign_service.create_campaign(prototype)

        return created_campaign.to_json(), 201

    def get_campaigns(self, req: request) -> (Page[Campaign], int):
        filters = req.args
        validate_pagination_filters(filters)
        campaigns_page = self.campaign_service.get_campaigns(filters)

        return campaigns_page.to_json(), 200

    def get_campaign_detail(self, req: request, campaign_id) -> (Campaign, int):
        campaign = self.campaign_service.get_campaign_detail(campaign_id)

        return campaign.to_json(), 200

    def create_campaign_model_image(self, campaign_id: int, req: request) -> (CampaignModelImage, int):
        return "jeje", 200
