from flask import Blueprint, current_app, request

from my_app.api import route

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')
pledgeBlueprint = Blueprint('pledgeController', __name__, url_prefix='/pledges')
orderBlueprint = Blueprint('orderController', __name__, url_prefix='/orders')
authBlueprint = Blueprint('authController', __name__, url_prefix='/auth')
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


@route(campaignBlueprint, '/<campaign_id>/orders', methods=['GET'])
def get_campaign_orders(campaign_id):
    return current_app.campaign_controller.get_campaign_orders(request, int(campaign_id))


# Pledges
@route(pledgeBlueprint, '/', methods=['POST'])
def create_pledge():
    return current_app.pledge_controller.create_pledge(request)


@route(pledgeBlueprint, '/<pledge_id>', methods=['DELETE'])
def cancel_pledge(pledge_id):
    return current_app.pledge_controller.cancel_pledge(request, int(pledge_id))


@route(pledgeBlueprint, '/', methods=['GET'])
def get_pledges():
    return current_app.pledge_controller.get_pledges(request)


# Orders
@route(orderBlueprint, '/status/massive', methods=['PATCH'])
def update_order_statuses():
    return current_app.order_controller.update_order_statuses_massively(request)


@route(orderBlueprint, '/<order_id>', methods=['PATCH'])
def update_order(order_id):
    return current_app.order_controller.update_order(request, int(order_id))


# Auth
@route(authBlueprint, '/login', methods=['POST'])
def login():
    return current_app.auth_controller.login(request)


@route(authBlueprint, '/signup/printer', methods=['POST'])
def create_printer():
    return current_app.auth_controller.create_printer(request)


@route(authBlueprint, '/signup/buyer', methods=['POST'])
def create_buyer():
    return current_app.auth_controller.create_buyer(request)
