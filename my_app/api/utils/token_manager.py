import datetime

import jwt

from my_app.api.exceptions import AuthException


class TokenManager:
    def __init__(self, secret_key: str):
        self._secret_key = secret_key

    def get_token_from_payload(self, payload: dict) -> str:
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        return jwt.encode(payload, self._secret_key, algorithm="HS256")

    def get_payload_from_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret_key, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise AuthException("Authorization token expired")
        except Exception as exc:
            raise AuthException("There is a problem with the authorization token: {}".format(str(exc)))
