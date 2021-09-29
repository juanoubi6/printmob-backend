import datetime
import enum
from typing import List, Optional

from my_app.api.domain.model_category import ModelCategory
from my_app.api.domain.model_file import ModelFile
from my_app.api.domain.designer import Designer
from my_app.api.domain.model_image import ModelImage


class ModelOrderingEnum(enum.Enum):
    MOST_LIKED = "Más populares"
    MOST_RECENT = "Más recientes"


class ModelOrdering:
    def __init__(
            self,
            value: str,
            name: str
    ):
        self.value = value
        self.name = name

    def to_json(self):
        return {
            "value": self.value,
            "name": self.name,
        }


class Model:
    def __init__(
            self,
            id: int,
            name: str,
            description: str,
            model_file: ModelFile,
            model_category: ModelCategory,
            width: int,
            length: int,
            depth: int,
            mp_preference_id: Optional[str],
            allow_purchases: bool,
            allow_alliances: bool,
            purchase_price: Optional[float],
            desired_percentage: Optional[float],
            model_images: List[ModelImage],
            designer: Designer,
            likes: int,
            liked_by_user: Optional[bool] = None,
            created_at: datetime.datetime = datetime.datetime.utcnow(),
            updated_at: datetime.datetime = datetime.datetime.utcnow(),
            deleted_at: datetime.datetime = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.model_file = model_file
        self.model_category = model_category
        self.width = width
        self.length = length
        self.depth = depth
        self.mp_preference_id = mp_preference_id
        self.allow_purchases = allow_purchases
        self.allow_alliances = allow_alliances
        self.purchase_price = purchase_price
        self.desired_percentage = desired_percentage
        self.model_images = model_images
        self.designer = designer
        self.likes = likes
        self.liked_by_user = liked_by_user
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model_file": self.model_file.to_json() if self.model_file is not None else None,
            "model_category": self.model_category.to_json() if self.model_category is not None else None,
            "width": self.width,
            "length": self.length,
            "depth": self.depth,
            "mp_preference_id": self.mp_preference_id,
            "allow_purchases": self.allow_purchases,
            "allow_alliances": self.allow_alliances,
            "purchase_price": self.purchase_price,
            "desired_percentage": self.desired_percentage,
            "model_images": [mi.to_json() for mi in self.model_images],
            "designer": self.designer.to_json() if self.designer is not None else None,
            "likes": self.likes,
            "liked_by_user": self.liked_by_user
        }


class ModelPrototype:
    def __init__(
            self,
            name: str,
            description: str,
            model_category_id: int,
            width: int,
            length: int,
            depth: int,
            allow_purchases: bool,
            allow_alliances: bool,
            purchase_price: Optional[float],
            desired_percentage: Optional[float],
            model_images_urls: List[str],
            designer_id: int,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.model_category_id = model_category_id
        self.width = width
        self.length = length
        self.depth = depth
        self.allow_purchases = allow_purchases
        self.allow_alliances = allow_alliances
        self.purchase_price = purchase_price
        self.desired_percentage = desired_percentage
        self.model_images_urls = model_images_urls
        self.designer_id = designer_id
