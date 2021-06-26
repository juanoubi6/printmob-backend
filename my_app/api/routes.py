from flask import Blueprint, current_app, request

from my_app.api import route

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')
pledgeBlueprint = Blueprint('pledgeController', __name__, url_prefix='/pledges')
healthBlueprint = Blueprint('healthController', __name__, url_prefix='/health')


# for load balancing purposes
@route(healthBlueprint, '/', methods=['GET'])
def healthy():
    return ''


# Campaigns
@route(campaignBlueprint, '/test-data', methods=['POST'])
def create_data():
    return current_app.campaign_controller.create_data(request)


@route(campaignBlueprint, '/', methods=['POST'])
def post_campaigns():
    return current_app.campaign_controller.post_campaign(request)


@route(campaignBlueprint, '/', methods=['GET'])
def get_campaigns():
    return current_app.campaign_controller.get_campaigns(request)


@route(campaignBlueprint, '/<campaign_id>', methods=['GET'])
def get_campaign_detail(campaign_id):
    return current_app.campaign_controller.get_campaign_detail(request, campaign_id)


@route(campaignBlueprint, '/<campaign_id>/model-images', methods=['POST'])
def create_campaign_model_image(campaign_id):
    return current_app.campaign_controller.create_campaign_model_image(request, int(campaign_id))


@route(campaignBlueprint, '/<campaign_id>/model-images/<campaign_model_image_id>', methods=['DELETE'])
def delete_campaign_model_image(campaign_id, campaign_model_image_id):
    return current_app.campaign_controller.delete_campaign_model_image(
        request,
        int(campaign_id),
        int(campaign_model_image_id)
    )


@route(campaignBlueprint, '/<campaign_id>/buyers', methods=['GET'])
def get_campaign_buyers(campaign_id):
    return current_app.campaign_controller.get_campaign_buyers(request, int(campaign_id))


# Pledges
@route(pledgeBlueprint, '/', methods=['POST'])
def create_pledge():
    return current_app.pledge_controller.create_pledge(request)


@route(pledgeBlueprint, '/<pledge_id>', methods=['DELETE'])
def cancel_pledge(pledge_id):
    return current_app.pledge_controller.cancel_pledge(request, int(pledge_id))
