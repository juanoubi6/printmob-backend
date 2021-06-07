from my_app.api.controllers import CampaignController, PledgeController
from my_app.api.repositories import CampaignRepository, PledgeRepository
from my_app.api.repositories.campaign_model_image_repository import CampaignModelImageRepository
from my_app.api.repositories.printer_repository import PrinterRepository
from my_app.api.repositories.tech_details_repository import TechDetailsRepository
from my_app.api.services import CampaignService, PledgeService


def inject_controllers(app, db):
    app.campaign_controller = build_campaign_controller(db)
    app.pledge_controller = build_pledge_controller(db)


def build_campaign_controller(db):
    campaign_repository = CampaignRepository(db)
    campaign_model_image_repository = CampaignModelImageRepository(db)
    tech_details_repository = TechDetailsRepository(db)
    printer_repository = PrinterRepository(db)
    campaign_service = CampaignService(campaign_repository,
                                       campaign_model_image_repository,
                                       tech_details_repository,
                                       printer_repository)

    return CampaignController(campaign_service)


def build_pledge_controller(db):
    pledge_repository = PledgeRepository(db)
    pledge_service = PledgeService(pledge_repository)

    return PledgeController(pledge_service)
