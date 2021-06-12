from my_app.api.domain import Page, Campaign
from my_app.api.domain.campaign import CampaignPrototype
from my_app.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException

PRINTER_NOT_FOUND = 'Non-existent printer for campaign'


class CampaignService:
    def __init__(self,
                 campaign_repository,
                 printer_repository):
        self.campaign_repository = campaign_repository
        self.printer_repository = printer_repository

    def create_campaign(self, prototype: CampaignPrototype) -> Campaign:
        self._validate_campaign_printer(prototype)

        return self.campaign_repository.create_campaign(prototype)

    def _validate_campaign_printer(self, prototype):
        if not self.printer_repository.exists_printer(prototype.printer_id):
            raise UnprocessableEntityException(PRINTER_NOT_FOUND)

    def get_campaigns(self, filters: dict) -> Page[Campaign]:
        return self.campaign_repository.get_campaigns(filters)

    def get_campaign_detail(self, campaign_id) -> Campaign:
        return self.campaign_repository.get_campaign_detail(campaign_id)
