from my_app.api.controllers import CampaignController
from my_app.api.repositories import CampaignRepository
from my_app.api.services import CampaignService


def inject_controllers(app, db):
    app.campaign_controller = build_campaign_controller(db)


def build_campaign_controller(db):
    campaign_repository = CampaignRepository(db)
    campaign_service = CampaignService(campaign_repository)

    return CampaignController(campaign_service)
