from my_app.api.exceptions.base import AuthException


class GoogleValidationException(AuthException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
