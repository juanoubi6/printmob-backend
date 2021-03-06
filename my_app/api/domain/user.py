import datetime
import enum
from typing import Optional


class UserType(enum.Enum):
    PRINTER = "Printer"
    BUYER = "Buyer"
    DESIGNER = "Designer"


class User:
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            user_name: str,
            date_of_birth: datetime.datetime,
            email: str,
            user_type: UserType,
            profile_picture_url: Optional[str],
            created_at: datetime.datetime = datetime.datetime.utcnow(),
            updated_at: datetime.datetime = datetime.datetime.utcnow(),
            deleted_at: datetime.datetime = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.user_type = user_type
        self.profile_picture_url = profile_picture_url
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "user_type": self.user_type.value,
            "profile_picture_url": self.profile_picture_url
        }

    def identity_data(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_type": self.user_type.value
        }


class UserPrototype:
    def __init__(
            self,
            first_name: str,
            last_name: str,
            user_name: str,
            date_of_birth: datetime.datetime,
            email: str,
            user_type: UserType,
            profile_picture_url: Optional[str],
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.user_type = user_type
        self.profile_picture_url = profile_picture_url
