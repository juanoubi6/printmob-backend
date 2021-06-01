import datetime
from typing import List

from my_app.api.domain.campaign_model_image import CampaignModelImage
from my_app.api.domain.printer import Printer
from my_app.api.domain.tech_detail import TechDetail
from my_app.api.domain.user import User
from my_app.api.repositories.models import CampaignModel

CampaignModelImages = List[CampaignModelImage]


class Campaign:
    def __init__(
            self,
            id: int,
            name: str,
            description: str,
            campaign_picture_url: str,
            campaign_model_images: CampaignModelImages,
            printer: Printer,
            pledge_price: float,
            start_date: datetime.datetime,
            end_date: datetime.datetime,
            min_pledgers: int,
            max_pledgers: int,
            current_pledgers: int,
            tech_details: TechDetail
    ):
        self.id = id
        self.name = name
        self.description = description
        self.campaign_picture_url = campaign_picture_url
        self.campaign_model_images = campaign_model_images
        self.printer = printer
        self.pledge_price = pledge_price
        self.start_date = start_date
        self.end_date = end_date
        self.min_pledgers = min_pledgers
        self.max_pledgers = max_pledgers
        self.current_pledgers = current_pledgers
        self.tech_details = tech_details

    @staticmethod
    def from_model(campaign_model: CampaignModel):
        return Campaign(
            id=campaign_model.id,
            name=campaign_model.name,
            description=campaign_model.description,
            campaign_picture_url=campaign_model.campaign_picture_url,
            campaign_model_images=list(map(lambda ci: CampaignModelImage.from_model(ci), campaign_model.images)),
            printer=Printer(User.from_model(campaign_model.printer.user)),
            pledge_price=float(campaign_model.pledge_price),
            start_date=campaign_model.start_date,
            end_date=campaign_model.end_date,
            min_pledgers=campaign_model.min_pledgers,
            max_pledgers=campaign_model.max_pledgers,
            current_pledgers=len(campaign_model.pledges),
            tech_details=TechDetail.from_model(campaign_model.tech_detail)
        )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "campaign_picture_url": self.campaign_picture_url,
            "campaign_model_images": list(map(lambda cmi: cmi.to_json(), self.campaign_model_images)),
            "printer": self.printer.to_json(),
            "pledge_price": self.pledge_price,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "min_pledgers": self.min_pledgers,
            "max_pledgers": self.max_pledgers,
            "current_pledgers": self.current_pledgers,
            "tech_details": self.tech_details.to_json()
        }
