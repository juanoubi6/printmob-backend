import json
from datetime import datetime

from flask import request

from my_app.api.domain import UserType, User, PrinterPrototype, UserPrototype, BankInformationPrototype, BuyerPrototype, \
    AddressPrototype, Balance, DesignerPrototype
from my_app.api.exceptions import AuthException, BusinessException
from my_app.api.services import UserService

USER_MISMATCH_ERROR = "Tu usuario no tiene permisos para acceder a esta información"
INVALID_USER_TYPE_ERROR = "El tipo de usuario es inválido"
BUYER_BALANCE_ERROR = "Los usuarios del tipo 'Comprador' no poseen balance"


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user_data_dashboard(self, req: request, user_id: int, user_data: dict) -> (dict, int):
        if user_id != int(user_data["id"]):
            raise AuthException(USER_MISMATCH_ERROR)

        if user_data["user_type"] == UserType.PRINTER.value:
            data_dashboard = self.user_service.get_printer_data_dashboard(user_id)
        elif user_data["user_type"] == UserType.DESIGNER.value:
            data_dashboard = self.user_service.get_designer_data_dashboard(user_id)
        elif user_data["user_type"] == UserType.BUYER.value:
            data_dashboard = self.user_service.get_buyer_data_dashboard(user_id)
        else:
            raise BusinessException(INVALID_USER_TYPE_ERROR)

        return data_dashboard.to_json(), 200

    def get_user_profile(self, req: request, user_id: int, user_data: dict) -> (User, int):
        if user_id != int(user_data["id"]):
            raise AuthException(USER_MISMATCH_ERROR)

        if user_data["user_type"] == UserType.PRINTER.value:
            user = self.user_service.get_printer_by_email(user_data["email"])
        elif user_data["user_type"] == UserType.BUYER.value:
            user = self.user_service.get_buyer_by_email(user_data["email"])
        elif user_data["user_type"] == UserType.DESIGNER.value:
            user = self.user_service.get_designer_by_email(user_data["email"])
        else:
            raise BusinessException(INVALID_USER_TYPE_ERROR)

        return user.to_json(), 200

    def update_user_profile(self, req: request, user_id: int, user_data: dict) -> (User, int):
        if user_id != int(user_data["id"]):
            raise AuthException(USER_MISMATCH_ERROR)

        body = json.loads(req.data)

        if user_data["user_type"] == UserType.PRINTER.value:
            prototype = self._generate_printer_prototype(body)
            updated_user = self.user_service.update_printer(user_id, prototype)
        elif user_data["user_type"] == UserType.BUYER.value:
            prototype = self._generate_buyer_prototype(body)
            updated_user = self.user_service.update_buyer(user_id, prototype)
        elif user_data["user_type"] == UserType.DESIGNER.value:
            prototype = self._generate_designer_prototype(body)
            updated_user = self.user_service.update_designer(user_id, prototype)
        else:
            raise BusinessException(INVALID_USER_TYPE_ERROR)

        return updated_user.to_json(), 200

    def get_user_balance(self, req: request, user_id: int, user_data: dict) -> (Balance, int):
        if user_id != int(user_data["id"]):
            raise AuthException(USER_MISMATCH_ERROR)

        if user_data["user_type"] == UserType.BUYER.value:
            raise BusinessException(BUYER_BALANCE_ERROR)

        balance = self.user_service.get_user_balance(user_id)

        return balance.to_json(), 200

    def request_balance(self, req: request, user_id: int, user_data: dict) -> (dict, int):
        if user_id != int(user_data["id"]):
            raise AuthException(USER_MISMATCH_ERROR)

        if user_data["user_type"] == UserType.BUYER.value:
            raise BusinessException(BUYER_BALANCE_ERROR)

        self.user_service.request_balance(user_id)

        return {"status": "ok"}, 200

    def _generate_printer_prototype(self, body: dict) -> PrinterPrototype:
        return PrinterPrototype(
            user_prototype=UserPrototype(
                first_name=body["first_name"],
                last_name=body["last_name"],
                user_name=body["user_name"],
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=body["email"],
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

    def _generate_buyer_prototype(self, body: dict) -> BuyerPrototype:
        return BuyerPrototype(
            user_prototype=UserPrototype(
                first_name=body["first_name"],
                last_name=body["last_name"],
                user_name=body["user_name"],
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=body["email"],
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

    def _generate_designer_prototype(self, body: dict) -> DesignerPrototype:
        return DesignerPrototype(
            user_prototype=UserPrototype(
                first_name=body["first_name"],
                last_name=body["last_name"],
                user_name=body["user_name"],
                date_of_birth=datetime.strptime(body["date_of_birth"], '%d-%m-%Y'),
                email=body["email"],
                user_type=UserType.DESIGNER,
                profile_picture_url=body.get("profile_picture_url", None)
            ),
            bank_information_prototype=BankInformationPrototype(
                cbu=body["bank_information"]["cbu"],
                bank=body["bank_information"]["bank"],
                account_number=body["bank_information"]["account_number"],
                alias=body["bank_information"]["alias"]
            )
        )
