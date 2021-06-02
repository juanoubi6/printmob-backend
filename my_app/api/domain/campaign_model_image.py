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

    def to_json(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "model_picture_url": self.model_picture_url,
        }
