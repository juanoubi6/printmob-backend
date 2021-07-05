import json

from flask import request

from my_app.api.domain import Printer
from my_app.api.exceptions import AuthException
from my_app.api.services import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self, req: request) -> (dict, int):
        body = json.loads(req.data)
        auth_token = body.get("token", None)

        if auth_token is None:
            raise AuthException("Authorization token was not provided")

        user_data, token = self.auth_service.get_user_login_data(auth_token)

        return {
                   "user_data": user_data.to_json(),
                   "type": user_data.user_type.value,
                   "token": token
               }, 200

    def create_printer(self, req: request) -> (Printer, int):
        pass
