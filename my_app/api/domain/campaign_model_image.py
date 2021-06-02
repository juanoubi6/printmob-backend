from my_app.api.repositories.models import CampaignModelImageModel


class CampaignModelImage:
    def __init__(
            self,
            id: int,
            model_picture_url: str,
            campaign_id: int
    ):
        self.id = id
        self.model_picture_url = model_picture_url
        self.campaign_id = campaign_id

    @staticmethod
    def from_model(campaign_model_image: CampaignModelImageModel):
        return CampaignModelImage(
            id=campaign_model_image.id,
            model_picture_url=campaign_model_image.model_picture_url,
            campaign_id=campaign_model_image.campaign_id
        )

    def to_json(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "model_picture_url": self.model_picture_url,
        }
