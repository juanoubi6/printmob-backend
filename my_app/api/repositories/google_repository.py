import logging
import time

import cachecontrol
import google.auth.transport.requests
import requests
from google.auth.transport.requests import Request, TimeoutGuard
from google.oauth2 import id_token

from my_app.api.domain import GoogleUserData
from my_app.api.exceptions import GoogleValidationException, AuthException, GoogleTimeoutException

GOOGLE_ISSUER = "accounts.google.com"


class GoogleRepository:
    def __init__(self, client_id: str, fallback_url: str):
        self.client_id = client_id
        self.google_fallback_url = fallback_url
        self._cached_session = cachecontrol.CacheControl(requests.sessions.Session())

    def warm_up(self):
        request = Request(session=self._cached_session)
        try:
            print("Warming up google client")
            # Execute request so Google Certificates are downloaded
            id_token.verify_oauth2_token("token", request, self.client_id)
            print("Finished warm up of google client")
        except Exception as exc:
            logging.info("Google Repository warm up exception: {}".format(str(exc)))

    def retrieve_token_data(self, token: str) -> GoogleUserData:
        request = google.auth.transport.requests.Request(session=self._cached_session)

        try:
            with TimeoutGuard(2, timeout_error_type=GoogleTimeoutException):
                token_data = id_token.verify_oauth2_token(token, request, self.client_id)
        except GoogleTimeoutException:
            token_data = self._fallback_token_validation(token)
        except Exception as exc:
            raise GoogleValidationException(
                "Unexpected error while retrieving token data from Google: {}".format(str(exc)))

        self._validate_token_data(token_data)

        return GoogleUserData(
            first_name=token_data["given_name"],
            last_name=token_data["family_name"],
            email=token_data["email"],
            picture=token_data["picture"]
        )

    def _validate_token_data(self, token_data: dict):
        if token_data["aud"] != self.client_id:
            raise AuthException("Invalid token. Audit failed")

        if token_data["iss"] != GOOGLE_ISSUER:
            raise AuthException("Invalid token. Bad issuer")

        if int(token_data["exp"]) < time.time():
            raise AuthException("Invalid token. Token already expired")

    def _fallback_token_validation(self, token) -> dict:
        response = requests.get(self.google_fallback_url + "?id_token={}".format(token))

        if response.status_code != 200:
            raise AuthException("Invalid token. Error: {}".format(response.json()["error_description"]))

        return response.json()
