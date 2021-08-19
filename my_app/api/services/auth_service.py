from my_app.api.domain import UserType, User
from my_app.api.exceptions import AuthException, BusinessException
from my_app.api.repositories import GoogleRepository, UserRepository
from my_app.api.utils.token_manager import TokenManager


class AuthService:
    def __init__(
            self,
            google_repository: GoogleRepository,
            user_repository: UserRepository,
            token_manager: TokenManager
    ):
        self.google_repository = google_repository
        self.user_repository = user_repository
        self.token_manager = token_manager

    def get_user_login_data(self, auth_token: str) -> (User, str):
        google_user_data = self.google_repository.retrieve_token_data(auth_token)
        user_data = self.user_repository.get_user_by_email(google_user_data.email)

        if user_data is None:
            raise AuthException("El usuario no se encuentra registrado")

        if user_data.user_type is UserType.PRINTER:
            printer = self.user_repository.get_printer_by_email(user_data.email)
            return printer, self.token_manager.get_token_from_payload(printer.identity_data())
        elif user_data.user_type is UserType.BUYER:
            buyer = self.user_repository.get_buyer_by_email(user_data.email)
            return buyer, self.token_manager.get_token_from_payload(buyer.identity_data())
        else:
            raise BusinessException("El tipo de usuario es inválido")
