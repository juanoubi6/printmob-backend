import logging

from flask import request


class TestController:
    def __init__(self, test_service):
        self.test_service = test_service

    def get_test_data(self, req: request):
        logging.info(req.base_url)
        logging.info(req.path)
        user = self.test_service.get_test_data_from_service()

        return user.to_json(), 201
