from my_app.api.domain import CampaignModelImage
from my_app.api.repositories.models import CampaignModelImageModel


class CampaignModelImageRepository:
    def __init__(self, db):
        self.db = db

    def create_campaign_model_image(self, campaign_id: int, image_url: str) -> CampaignModelImage:
        campaign_model_image_model = CampaignModelImageModel(campaign_id=campaign_id,
                                                             model_picture_url=image_url)
        self.db.session.add(campaign_model_image_model)
        self.db.session.commit()

        return campaign_model_image_model.to_campaign_model_image_entity()
