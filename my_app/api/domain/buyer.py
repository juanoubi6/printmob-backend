from my_app.api.domain import Address
from my_app.api.domain.user import User


class Buyer(User):
    def __init__(self, user: User, address: Address):
        super().__init__(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name,
            date_of_birth=user.date_of_birth,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at
        )
        self.address = address

    def to_json(self):
        json_dict = User.to_json(self)
        json_dict["address"] = self.address.to_json()

        return json_dict
