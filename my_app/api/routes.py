from flask import Blueprint, current_app, request

from my_app.api import route

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')
pledgeBlueprint = Blueprint('pledgeController', __name__, url_prefix='/pledges')


@route(campaignBlueprint, '/', methods=['POST'])
def post_campaigns():
    return current_app.campaign_controller.post_campaign(request)


@route(campaignBlueprint, '/', methods=['GET'])
def get_campaigns():
    return current_app.campaign_controller.get_campaigns(request)


@route(campaignBlueprint, '/<campaign_id>', methods=['GET'])
def get_campaign_detail(campaign_id):
    return current_app.campaign_controller.get_campaign_detail(request, campaign_id)


@route(pledgeBlueprint, '/', methods=['POST'])
def create_pledge():
    return current_app.pledge_controller.create_pledge(request)
