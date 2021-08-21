import json
from datetime import datetime

from flask import request

from my_app.api.domain import Printer, PrinterPrototype, UserPrototype, UserType, Buyer, BuyerPrototype, \
    AddressPrototype, BankInformationPrototype
from my_app.api.exceptions import InvalidFieldException, InvalidParamException
from my_app.api.services import AuthService, UserService


class AuthController:
    def __init__(self, auth_service: AuthService, user_service: UserService):
        self.auth_service = auth_service
        self.user_service = user_service

    def login(self, req: request) -> (dict, int):
        body = json.loads(req.data)
        auth_token = body.get("token", None)

        if auth_token is None:
            raise InvalidFieldException("El token de autorización no fue provisto")

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
                user_name=str(body["user_name"]).lower(),
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=str(body["email"]).lower(),
                user_type=UserType.PRINTER,
                profile_picture_url=body.get("profile_picture_url", None)
            ),
            bank_information_prototype=BankInformationPrototype(
                cbu=body["bank_information"]["cbu"],
                bank=body["bank_information"]["bank"],
                account_number=body["bank_information"]["account_number"],
                alias=body["bank_information"]["alias"]
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
                user_name=str(body["user_name"]).lower(),
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=str(body["email"]).lower(),
                user_type=UserType.BUYER,
                profile_picture_url=body.get("profile_picture_url", None)
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

    def validate_user_data(self, req: request) -> (dict, int):
        body = json.loads(req.data)

        user_name = body.get("user_name", None)
        email = body.get("email", None)

        if user_name is None or email is None:
            raise InvalidParamException("El nombre de usuario o email no fueron completados")

        exist = self.user_service.validate_user_name_and_email_existence(user_name, email)

        return exist, 200
