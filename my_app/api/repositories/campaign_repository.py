from sqlalchemy import desc

from my_app.api.domain import Campaign
from my_app.api.repositories.models import CampaignModel


class CampaignRepository:
    def __init__(self, db):
        self.db = db

    def get_campaigns(self):
        campaign_model = CampaignModel(name='Name')
        self.db.session.add(campaign_model)
        self.db.session.commit()

        campaign_model = self.db.session.query(CampaignModel).filter_by(name='Name').order_by(
            desc(CampaignModel.id)).first()
        return [Campaign(campaign_model.name, campaign_model.id)]
