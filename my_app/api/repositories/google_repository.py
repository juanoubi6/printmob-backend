import http
import logging
import time
from concurrent.futures import Executor, TimeoutError

import cachecontrol
import google.auth.transport.requests
import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from my_app.api.domain import GoogleUserData
from my_app.api.exceptions import GoogleValidationException, AuthException

GOOGLE_ISSUER = "accounts.google.com"


class GoogleRepository:
    def __init__(self, client_id: str, fallback_url: str, executor: Executor):
        self.client_id = client_id
        self.google_fallback_url = fallback_url
        self._cached_session = cachecontrol.CacheControl(requests.sessions.Session())
        self.executor = executor

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
            future = self.executor.submit(id_token.verify_oauth2_token, token, request, self.client_id)
            token_data = future.result(2)
        except TimeoutError:
            token_data = self._fallback_token_validation(token)
        except Exception as exc:
            raise GoogleValidationException(
                "Error inesperado al validar los datos de su token de autenticación contra Google: {}".format(str(exc)))

        self._validate_token_data(token_data)

        return GoogleUserData(
            first_name=token_data["given_name"],
            last_name=token_data["family_name"],
            email=token_data["email"],
            picture=token_data["picture"]
        )

    def _validate_token_data(self, token_data: dict):
        if token_data["aud"] != self.client_id:
            raise AuthException("Token inválido. Audit failed")

        if token_data["iss"] != GOOGLE_ISSUER:
            raise AuthException("Token inválido. Bad issuer")

        if int(token_data["exp"]) < time.time():
            raise AuthException("El token ya ha expirado")

    def _fallback_token_validation(self, token) -> dict:
        response = requests.get(self.google_fallback_url + "?id_token={}".format(token), timeout=2)

        if response.status_code != http.HTTPStatus.OK:
            raise GoogleValidationException("Token inválido. Error: {}".format(response.json()["error_description"]))

        return response.json()
