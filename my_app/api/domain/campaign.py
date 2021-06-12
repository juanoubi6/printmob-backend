import datetime
from typing import List

from my_app.api.domain.campaign_model_image import CampaignModelImage
from my_app.api.domain.printer import Printer
from my_app.api.domain.tech_detail import TechDetail, TechDetailPrototype


class Campaign:
    def __init__(
            self,
            id: int,
            name: str,
            description: str,
            campaign_picture_url: str,
            campaign_model_images: List[CampaignModelImage],
            printer: Printer,
            pledge_price: float,
            end_date: datetime.datetime,
            min_pledgers: int,
            max_pledgers: int,
            current_pledgers: int,
            tech_details: TechDetail,
            created_at: datetime.datetime = datetime.datetime.utcnow(),
            updated_at: datetime.datetime = datetime.datetime.utcnow(),
            deleted_at: datetime.datetime = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.campaign_picture_url = campaign_picture_url
        self.campaign_model_images = campaign_model_images
        self.printer = printer
        self.pledge_price = pledge_price
        self.end_date = end_date
        self.min_pledgers = min_pledgers
        self.max_pledgers = max_pledgers
        self.current_pledgers = current_pledgers
        self.tech_details = tech_details
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "campaign_picture_url": self.campaign_picture_url,
            "campaign_model_images": list(map(lambda cmi: cmi.to_json(), self.campaign_model_images)),
            "printer": self.printer.to_json() if self.printer is not None else None,
            "pledge_price": self.pledge_price,
            "end_date": self.end_date,
            "min_pledgers": self.min_pledgers,
            "max_pledgers": self.max_pledgers,
            "current_pledgers": self.current_pledgers,
            "tech_details": self.tech_details.to_json() if self.tech_details is not None else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }


class CampaignPrototype:
    def __init__(
            self,
            name: str,
            description: str,
            campaign_picture_url: str,
            campaign_model_image_urls: List[str],
            printer_id: int,
            pledge_price: float,
            end_date: datetime.datetime,
            min_pledgers: int,
            max_pledgers: int,
            tech_details: TechDetailPrototype
    ):
        self.id = id
        self.name = name
        self.description = description
        self.campaign_picture_url = campaign_picture_url
        self.campaign_model_image_urls = campaign_model_image_urls
        self.printer_id = printer_id
        self.pledge_price = pledge_price
        self.end_date = end_date
        self.min_pledgers = min_pledgers
        self.max_pledgers = max_pledgers
        self.tech_details = tech_details
