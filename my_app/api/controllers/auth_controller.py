import json
from datetime import datetime

from flask import request

from my_app.api.domain import Printer, PrinterPrototype, UserPrototype, UserType, Buyer, BuyerPrototype, \
    AddressPrototype
from my_app.api.exceptions import AuthException
from my_app.api.services import AuthService, UserService


class AuthController:
    def __init__(self, auth_service: AuthService, user_service: UserService):
        self.auth_service = auth_service
        self.user_service = user_service

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
        body = json.loads(req.data)

        prototype = PrinterPrototype(
            user_prototype=UserPrototype(
                first_name=body["first_name"],
                last_name=body["last_name"],
                user_name=body["user_name"],
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=body["email"],
                user_type=UserType.PRINTER
            )
        )

        printer = self.user_service.create_printer(prototype)

        return printer.to_json(), 201

    def create_buyer(self, req: request) -> (Buyer, int):
        body = json.loads(req.data)

        prototype = BuyerPrototype(
            user_prototype=UserPrototype(
                first_name=body["first_name"],
                last_name=body["last_name"],
                user_name=body["user_name"],
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=body["email"],
                user_type=UserType.BUYER
            ),
            address_prototype=AddressPrototype(
                address=body["address"]["address"],
                zip_code=body["address"]["zip_code"],
                province=body["address"]["province"],
                city=body["address"]["city"],
                floor=body["address"]["floor"],
                apartment=body["address"]["apartment"],
            )
        )

        buyer = self.user_service.create_buyer(prototype)

        return buyer.to_json(), 201
