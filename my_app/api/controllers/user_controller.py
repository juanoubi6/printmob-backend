from flask import request

from my_app.api.domain import UserType, User
from my_app.api.exceptions import AuthException, BusinessException
from my_app.api.services import UserService


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user_profile(self, req: request, user_id: int, user_data: dict) -> (User, int):
        if user_id != user_data["id"]:
            raise AuthException("Identified user and user_id do not match")

        if user_data["user_type"] == UserType.PRINTER.value:
            user = self.user_service.get_printer_by_email(user_data["email"])
        elif user_data["user_type"] == UserType.BUYER.value:
            user = self.user_service.get_buyer_by_email(user_data["email"])
        else:
            raise BusinessException("Invalid user type from access token")

        return user.to_json(), 200

