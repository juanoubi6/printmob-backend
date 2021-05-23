from flask import Blueprint, current_app, request

from my_app.api import route

bp = Blueprint('testController', __name__, url_prefix='/test-controller')


@route(bp, '/testUrl', methods=['GET'])
def get_test_data():
    return current_app.test_controller.get_test_data(request)
