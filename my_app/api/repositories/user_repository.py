from my_app.api.domain import Printer, Buyer, User
from my_app.api.repositories.models import PrinterModel, UserModel


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

    def _get_user_model_by_email(self, email: str) -> UserModel:
        return self.db.session.query(UserModel).filter_by(email=email).first()
