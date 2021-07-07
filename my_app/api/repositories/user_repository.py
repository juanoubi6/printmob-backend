from my_app.api.domain import Printer, Buyer, User, BuyerPrototype, PrinterPrototype, UserPrototype
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
