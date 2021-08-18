from datetime import timedelta

from mercadopago import SDK

from my_app.api.domain import Campaign, Payment
from my_app.api.exceptions import MercadopagoException


class MercadopagoRepository:
    def __init__(self, sdk: SDK, error_back_url: str, pledge_success_back_url):
        self._sdk = sdk
        self._error_back_url = error_back_url
        self._pledge_success_back_url = pledge_success_back_url

    def create_campaign_pledge_preference(self, campaign: Campaign) -> int:
        try:
            preference_data = {
                "items": [
                    {
                        "title": campaign.name,
                        "description": campaign.description,
                        "quantity": 1,
                        "unit_price": campaign.pledge_price,
                        "currency_id": "ARS",
                    }
                ],
                "external_reference": str(campaign.id),
                "expires": True,
                "expiration_date_to": (campaign.end_date + timedelta(days=1)).isoformat(),
                "payment_methods": {
                    "excluded_payment_types": [{"id": "ticket"}]
                },
                "auto_return": "approved",
                "back_urls": {
                    "success": self._pledge_success_back_url,
                    "failure": self._error_back_url,
                },
            }

            preference_response = self._sdk.preference().create(preference_data)
            if preference_response["status"] > 201:
                raise Exception(preference_response["response"]["message"])

            preference = preference_response["response"]
        except Exception as exc:
            raise MercadopagoException("Failed to create campaign pledge preference: {}".format(str(exc)))

        return preference["id"]

    def get_payment_data(self, payment_id: int) -> Payment:
        try:
            payment_response = self._sdk.payment().get(payment_id)
            if payment_response["status"] != 200:
                raise Exception(payment_response["response"]["message"])

            payment = payment_response["response"]
        except Exception as exc:
            raise MercadopagoException("Failed to retrieve payment {} data: {}".format(payment_id, str(exc)))

        return Payment(payment_id=payment_id, payment_data=payment)

    def refund_payment(self, payment_id: int):
        try:
            refund_response = self._sdk.refund().create(payment_id)
            if refund_response["status"] > 200:
                raise Exception(refund_response["response"]["message"])
        except Exception as exc:
            if "live credentials" in str(exc):
                return
            raise MercadopagoException("Failed to refund payment {}: {}".format(payment_id, str(exc)))
