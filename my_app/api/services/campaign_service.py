class CampaignService:
    def __init__(self, campaign_repository):
        self.campaign_repository = campaign_repository

    def get_campaigns(self):
        return self.campaign_repository.get_campaigns()

    def get_campaign_detail(self, campaign_id):
        return self.campaign_repository.get_campaign_detail(campaign_id)
