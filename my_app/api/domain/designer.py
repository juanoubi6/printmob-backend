from my_app.api.domain import BankInformationPrototype, BankInformation
from my_app.api.domain.user import User, UserType, UserPrototype


class Designer(User):
    def __init__(self, user: User, bank_information: BankInformation):
        super().__init__(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name,
            date_of_birth=user.date_of_birth,
            email=user.email,
            user_type=UserType.DESIGNER,
            profile_picture_url=user.profile_picture_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at
        )
        self.bank_information = bank_information

    def to_json(self):
        json_dict = User.to_json(self)
        json_dict["bank_information"] = self.bank_information.to_json()

        return json_dict


class DesignerPrototype:
    def __init__(self, user_prototype: UserPrototype, bank_information_prototype: BankInformationPrototype):
        self.user_prototype = user_prototype
        self.bank_information_prototype = bank_information_prototype
