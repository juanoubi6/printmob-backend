from my_app.api.domain import PrinterPrototype, Printer, BuyerPrototype, Buyer, \
    UserPrototype, AddressPrototype
from my_app.api.exceptions import BusinessException
from my_app.api.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_printer(self, prototype: PrinterPrototype) -> Printer:
        self._validate_user_data(prototype.user_prototype)

        return self.user_repository.create_printer(prototype)

    def create_buyer(self, prototype: BuyerPrototype) -> Buyer:
        self._validate_user_data(prototype.user_prototype)
        self._validate_user_address(prototype.address_prototype)

        return self.user_repository.create_buyer(prototype)

    def _validate_user_data(self, prototype: UserPrototype):
        if self.user_repository.is_user_name_in_use(prototype.user_name):
            raise BusinessException("Username already in use")

        if self.user_repository.is_email_in_use(prototype.email):
            raise BusinessException("Email already in use")

    def _validate_user_address(self, prototype: AddressPrototype):
        pass
