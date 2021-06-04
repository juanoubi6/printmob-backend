from my_app.api.controllers import CampaignController, PledgeController
from my_app.api.repositories import CampaignRepository, PledgeRepository
from my_app.api.services import CampaignService, PledgeService


def inject_controllers(app, db):
    app.campaign_controller = build_campaign_controller(db)
    app.pledge_controller = build_pledge_controller(db)


def build_campaign_controller(db):
    campaign_repository = CampaignRepository(db)
    campaign_service = CampaignService(campaign_repository)

    return CampaignController(campaign_service)


def build_pledge_controller(db):
    pledge_repository = PledgeRepository(db)
    pledge_service = PledgeService(pledge_repository)

    return PledgeController(pledge_service)
