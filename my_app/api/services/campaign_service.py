from my_app.api.domain import Page, Campaign


class CampaignService:
    def __init__(self, campaign_repository):
        self.campaign_repository = campaign_repository

    def get_campaigns(self, filters: dict) -> Page[Campaign]:
        return self.campaign_repository.get_campaigns(filters)

    def get_campaign_detail(self, campaign_id) -> Campaign:
        return self.campaign_repository.get_campaign_detail(campaign_id)
