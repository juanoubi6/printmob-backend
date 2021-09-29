from concurrent.futures import Executor

from my_app.api.domain import PrinterPrototype, Printer, BuyerPrototype, Buyer, \
    UserPrototype, AddressPrototype, BankInformationPrototype, Balance, DesignerPrototype, Designer, \
    PrinterDataDashboard, DesignerDataDashboard, BuyerDataDashboard
from my_app.api.exceptions import BusinessException
from my_app.api.repositories import UserRepository, TransactionRepository, EmailRepository
from my_app.api.utils.email import create_money_request_email


class UserService:
    def __init__(
            self,
            user_repository: UserRepository,
            transaction_repository: TransactionRepository,
            email_repository: EmailRepository,
            executor: Executor
    ):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.email_repository = email_repository
        self.executor = executor

    def get_printer_data_dashboard(self, printer_id: int) -> PrinterDataDashboard:
        return self.user_repository.get_printer_data_dashboard(printer_id)

    def get_designer_data_dashboard(self, designer_id: int) -> DesignerDataDashboard:
        return self.user_repository.get_designer_data_dashboard(designer_id)

    def get_buyer_data_dashboard(self, buyer_id: int) -> BuyerDataDashboard:
        return self.user_repository.get_buyer_data_dashboard(buyer_id)

    def create_printer(self, prototype: PrinterPrototype) -> Printer:
        self._validate_user_data(prototype.user_prototype)
        self._validate_bank_information(prototype.bank_information_prototype)

        return self.user_repository.create_printer(prototype)

    def get_printer_by_email(self, email: str) -> Printer:
        return self.user_repository.get_printer_by_email(email)

    def update_printer(self, printer_id: int, prototype: PrinterPrototype) -> Printer:
        return self.user_repository.update_printer(printer_id, prototype)

    def create_buyer(self, prototype: BuyerPrototype) -> Buyer:
        self._validate_user_data(prototype.user_prototype)
        self._validate_user_address(prototype.address_prototype)

        return self.user_repository.create_buyer(prototype)

    def get_buyer_by_email(self, email: str) -> Buyer:
        return self.user_repository.get_buyer_by_email(email)

    def update_buyer(self, buyer_id: int, prototype: BuyerPrototype) -> Buyer:
        return self.user_repository.update_buyer(buyer_id, prototype)

    def create_designer(self, prototype: DesignerPrototype) -> Designer:
        self._validate_user_data(prototype.user_prototype)
        self._validate_bank_information(prototype.bank_information_prototype)

        return self.user_repository.create_designer(prototype)

    def get_designer_by_email(self, email: str) -> Designer:
        return self.user_repository.get_designer_by_email(email)

    def update_designer(self, buyer_id: int, prototype: DesignerPrototype) -> Designer:
        return self.user_repository.update_designer(buyer_id, prototype)

    def get_user_balance(self, user_id: int) -> Balance:
        return self.transaction_repository.get_user_balance(user_id)

    def request_balance(self, user_id: int):
        requested_balance, send_notification = self.transaction_repository.create_balance_request(user_id)
        user = self.user_repository.get_user_by_id(user_id)

        if requested_balance != 0.0 and user is not None and send_notification:
            self.executor.submit(
                self.email_repository.send_individual_email,
                create_money_request_email(user.email, user, requested_balance)
            )

    def validate_user_name_and_email_existence(self, user_name: str, email: str) -> dict:
        return {
            "email": self.user_repository.is_email_in_use(email),
            "user_name": self.user_repository.is_user_name_in_use(user_name)
        }

    def _validate_user_data(self, prototype: UserPrototype):
        if self.user_repository.is_user_name_in_use(prototype.user_name):
            raise BusinessException("El nombre de usuario ya se encuentra en uso")

        if self.user_repository.is_email_in_use(prototype.email):
            raise BusinessException("El email ya se encuentra en uso")

    def _validate_user_address(self, prototype: AddressPrototype):
        pass

    def _validate_bank_information(self, prototype: BankInformationPrototype):
        pass
