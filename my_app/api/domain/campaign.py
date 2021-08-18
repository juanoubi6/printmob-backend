import datetime
import enum
from typing import List

from my_app.api.domain.campaign_model_image import CampaignModelImage
from my_app.api.domain.printer import Printer
from my_app.api.domain.tech_detail import TechDetail, TechDetailPrototype


class CampaignStatus(enum.Enum):
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    UNSATISFIED = "Unsatisfied"
    CONFIRMED = "Confirmed"
    TO_BE_FINALIZED = "To be finalized"
    TO_BE_CANCELLED = "To be cancelled"


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
            status: CampaignStatus,
            mp_preference_id: str,
            created_at: datetime.datetime = datetime.datetime.utcnow(),
            updated_at: datetime.datetime = datetime.datetime.utcnow(),
            deleted_at: datetime.datetime = None,
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
        self.status = status
        self.mp_preference_id = mp_preference_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def has_reached_confirmation_goal(self) -> bool:
        return self.current_pledgers >= self.min_pledgers

    def has_reached_end_date(self) -> bool:
        return datetime.datetime.now() > self.end_date

    def has_reached_maximum_pledgers(self) -> bool:
        if self.max_pledgers is None:
            return False
        else:
            return self.current_pledgers >= self.max_pledgers

    def has_one_pledge_left(self) -> bool:
        if self.max_pledgers is None:
            return False
        else:
            return self.max_pledgers - self.current_pledgers == 1

    def has_to_be_confirmed(self) -> bool:
        return (not self.has_one_pledge_left()) and (self.min_pledgers - self.current_pledgers == 1)

    def can_be_cancelled(self) -> bool:
        return self.status == CampaignStatus.IN_PROGRESS and self.current_pledgers < self.min_pledgers

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "campaign_picture_url": self.campaign_picture_url,
            "campaign_model_images": [cmi.to_json() for cmi in self.campaign_model_images],
            "printer": self.printer.to_json() if self.printer is not None else None,
            "pledge_price": self.pledge_price,
            "end_date": self.end_date,
            "min_pledgers": self.min_pledgers,
            "max_pledgers": self.max_pledgers,
            "current_pledgers": self.current_pledgers,
            "tech_details": self.tech_details.to_json() if self.tech_details is not None else None,
            "status": self.status.value,
            "mp_preference_id": self.mp_preference_id,
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
            tech_details: TechDetailPrototype,
            status: CampaignStatus
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
        self.status = status
