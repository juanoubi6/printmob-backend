from my_app.api.exceptions import BusinessException


class ModelCreationException(BusinessException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
