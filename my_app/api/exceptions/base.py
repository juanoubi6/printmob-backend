class BusinessException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ServerException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
