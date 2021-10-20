class CampaignModelImage:
    def __init__(
            self,
            id: int,
            model_picture_url: str,
            campaign_id: int,
            file_name: str
    ):
        self.id = id
        self.model_picture_url = model_picture_url
        self.campaign_id = campaign_id
        self.file_name = file_name

    def to_json(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "model_picture_url": self.model_picture_url,
        }


class CampaignModelImagePrototype:
    def __init__(
            self,
            model_picture_url: str,
            campaign_id: int,
            file_name: str
    ):
        self.model_picture_url = model_picture_url
        self.campaign_id = campaign_id
        self.file_name = file_name


class CampaignModelImageWithoutCampaignPrototype:
    def __init__(
            self,
            model_picture_url: str,
            file_name: str
    ):
        self.model_picture_url = model_picture_url
        self.file_name = file_name

