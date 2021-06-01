import datetime

from my_app.api.repositories.models import UserModel


class User:
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            user_name: str,
            date_of_birth: datetime.datetime,
            email: str
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.date_of_birth = date_of_birth
        self.email = email

    @staticmethod
    def from_model(user_model: UserModel):
        return User(
            id=user_model.id,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            user_name=user_model.user_name,
            date_of_birth=user_model.date_of_birth,
            email=user_model.email
        )

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email
        }
