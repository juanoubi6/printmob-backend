from flask import Blueprint, current_app, request

from my_app.api import route

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')


@route(campaignBlueprint, '/', methods=['GET'])
def get_campaigns():
    return current_app.campaign_controller.get_campaigns(request)
