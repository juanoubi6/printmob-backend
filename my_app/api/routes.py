from flask import Blueprint, current_app, request

from my_app.api import route
from my_app.api.exceptions.NotFoundException import NotFoundException

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')


@route(campaignBlueprint, '/', methods=['GET'])
def get_campaigns():
    return current_app.campaign_controller.get_campaigns(request)


@route(campaignBlueprint, '/<campaign_id>', methods=['GET'])
def get_campaign_detail(campaign_id):
    return current_app.campaign_controller.get_campaign_detail(request, campaign_id)
