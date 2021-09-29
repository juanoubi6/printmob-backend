from functools import wraps
from flask import request, current_app

from my_app.api.exceptions import AuthException

TOKEN_HEADER_NAME = "Authorization"


def validate_bearer_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if TOKEN_HEADER_NAME not in request.headers:
            raise AuthException("El token de autenticación no ha sido enviado")

        payload = current_app.token_manager.get_payload_from_token(request.headers.get(TOKEN_HEADER_NAME))

        return f(*args, **kwargs, user_data=payload)

    return decorated_function


def get_user_data_if_sent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if TOKEN_HEADER_NAME not in request.headers:
            return f(*args, **kwargs, user_data=None)

        payload = current_app.token_manager.get_payload_from_token(request.headers.get(TOKEN_HEADER_NAME))

        return f(*args, **kwargs, user_data=payload)

    return decorated_function
