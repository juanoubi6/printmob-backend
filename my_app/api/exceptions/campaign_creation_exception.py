from my_app.api.exceptions import BusinessException


class CampaignCreationException(BusinessException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
