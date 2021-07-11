import datetime

from my_app.api.domain import Printer, Buyer, User, BuyerPrototype, PrinterPrototype, UserPrototype
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories.models import PrinterModel, UserModel, BuyerModel, AddressModel, BankInformationModel


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_printer_by_email(self, email: str) -> Printer:
        user_model = self._get_user_model_by_email(email)

        return user_model.printer.to_printer_entity()

    def get_buyer_by_email(self, email: str) -> Buyer:
        user_model = self._get_user_model_by_email(email)

        return user_model.buyer.to_buyer_entity()

    def get_user_by_email(self, email: str) -> User:
        return self._get_user_model_by_email(email).to_user_entity()

    def is_user_name_in_use(self, user_name: str) -> bool:
        return self.db.session.query(UserModel).filter_by(user_name=user_name).first() is not None

    def is_email_in_use(self, email: str) -> bool:
        return self.db.session.query(UserModel).filter_by(email=email).first() is not None

    def create_buyer(self, prototype: BuyerPrototype) -> Buyer:
        user_model = self._create_user_model(prototype.user_prototype)
        self.db.session.add(user_model)

        address_model = AddressModel(
            address=prototype.address_prototype.address,
            zip_code=prototype.address_prototype.zip_code,
            province=prototype.address_prototype.province,
            city=prototype.address_prototype.city,
            floor=prototype.address_prototype.floor,
            apartment=prototype.address_prototype.apartment
        )
        self.db.session.add(address_model)
        self.db.session.flush()

        buyer_model = BuyerModel(id=user_model.id, address_id=address_model.id)
        self.db.session.add(buyer_model)
        self.db.session.commit()

        return buyer_model.to_buyer_entity()

    def update_buyer(self, buyer_id: int, prototype: BuyerPrototype) -> Buyer:
        buyer_model = self._get_buyer_model_by_id(buyer_id)
        if buyer_model is None:
            raise NotFoundException("Buyer could not be found")

        buyer_model.user.first_name = prototype.user_prototype.first_name
        buyer_model.user.last_name = prototype.user_prototype.last_name
        buyer_model.user.date_of_birth = prototype.user_prototype.date_of_birth
        buyer_model.user.updated_at = datetime.datetime.now()

        buyer_model.address.address = prototype.address_prototype.address
        buyer_model.address.zip_code = prototype.address_prototype.zip_code
        buyer_model.address.province = prototype.address_prototype.province
        buyer_model.address.city = prototype.address_prototype.city
        buyer_model.address.floor = prototype.address_prototype.floor
        buyer_model.address.apartment = prototype.address_prototype.apartment

        self.db.session.commit()

        return buyer_model.to_buyer_entity()

    def create_printer(self, prototype: PrinterPrototype) -> Printer:
        user_model = self._create_user_model(prototype.user_prototype)
        self.db.session.add(user_model)

        bank_information_model = BankInformationModel(
            cbu=prototype.bank_information_prototype.cbu,
            alias=prototype.bank_information_prototype.alias,
            bank=prototype.bank_information_prototype.bank,
            account_number=prototype.bank_information_prototype.account_number,
        )
        self.db.session.add(bank_information_model)
        self.db.session.flush()

        printer_model = PrinterModel(id=user_model.id, bank_information_id=bank_information_model.id)
        self.db.session.add(printer_model)
        self.db.session.commit()

        return printer_model.to_printer_entity()

    def update_printer(self, printer_id: int, prototype: PrinterPrototype) -> Printer:
        printer_model = self._get_printer_model_by_id(printer_id)
        if printer_model is None:
            raise NotFoundException("Printer could not be found")

        printer_model.user.first_name = prototype.user_prototype.first_name
        printer_model.user.last_name = prototype.user_prototype.last_name
        printer_model.user.date_of_birth = prototype.user_prototype.date_of_birth
        printer_model.user.updated_at = datetime.datetime.now()

        printer_model.bank_information.cbu = prototype.bank_information_prototype.cbu
        printer_model.bank_information.alias = prototype.bank_information_prototype.alias
        printer_model.bank_information.bank = prototype.bank_information_prototype.bank
        printer_model.bank_information.account_number = prototype.bank_information_prototype.account_number

        self.db.session.commit()

        return printer_model.to_printer_entity()

    def _create_user_model(self, prototype: UserPrototype) -> UserModel:
        user_model = UserModel(
            first_name=prototype.first_name,
            last_name=prototype.last_name,
            user_name=prototype.user_name,
            date_of_birth=prototype.date_of_birth,
            email=prototype.email,
            user_type=prototype.user_type.value
        )

        return user_model

    def _get_user_model_by_email(self, email: str) -> UserModel:
        return self.db.session.query(UserModel).filter_by(email=email).first()

    def _get_buyer_model_by_id(self, user_id: int) -> BuyerModel:
        return self.db.session.query(BuyerModel).filter_by(id=user_id).first()

    def _get_printer_model_by_id(self, user_id: int) -> PrinterModel:
        return self.db.session.query(PrinterModel).filter_by(id=user_id).first()
