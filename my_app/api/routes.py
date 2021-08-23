import datetime

from flask import Blueprint, current_app, request, make_response

from my_app.api import route
from my_app.api.controllers import validate_bearer_token

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')
buyerBlueprint = Blueprint('buyerBlueprint', __name__, url_prefix='/buyers')
pledgeBlueprint = Blueprint('pledgeController', __name__, url_prefix='/pledges')
orderBlueprint = Blueprint('orderController', __name__, url_prefix='/orders')
userBlueprint = Blueprint('userController', __name__, url_prefix='/users')
authBlueprint = Blueprint('authController', __name__, url_prefix='/auth')
healthBlueprint = Blueprint('healthController', __name__, url_prefix='/health')


# for load balancing purposes
@route(healthBlueprint, '/', methods=['GET'])
def healthy():
    return ''


########################### Testing endpoint ###########################
@route(campaignBlueprint, '/test-data', methods=['POST'])  # Testing-use
def create_data():
    return current_app.campaign_controller.create_data(request)


@route(campaignBlueprint, '/end-campaigns', methods=['POST'])  # Testing-use
def end_campaigns():
    return current_app.cron_controller.end_campaigns()


@route(userBlueprint, '/token', methods=['GET'])  # Testing-use
def get_token():
    payload = {
        "id": request.args["id"],
        "email": request.args["email"],
        "user_type": request.args["user_type"],
    }

    return current_app.token_manager.get_token_from_payload(payload)


########################### Testing endpoint ###########################

# Campaigns
@route(campaignBlueprint, '/', methods=['POST'])
@validate_bearer_token
def post_campaigns(user_data):
    return current_app.campaign_controller.post_campaign(request)


@route(campaignBlueprint, '/', methods=['GET'])
def get_campaigns():
    return current_app.campaign_controller.get_campaigns(request)


@route(campaignBlueprint, '/<campaign_id>', methods=['GET'])
def get_campaign_detail(campaign_id):
    return current_app.campaign_controller.get_campaign_detail(request, campaign_id)


@route(campaignBlueprint, '/<campaign_id>/model-images', methods=['POST'])
@validate_bearer_token
def create_campaign_model_image(campaign_id, user_data):
    return current_app.campaign_controller.create_campaign_model_image(request, int(campaign_id))


@route(campaignBlueprint, '/<campaign_id>/model-images/<campaign_model_image_id>', methods=['DELETE'])
def delete_campaign_model_image(campaign_id, campaign_model_image_id):
    return current_app.campaign_controller.delete_campaign_model_image(
        request,
        int(campaign_id),
        int(campaign_model_image_id)
    )


# TODO: Add auth decorator and validate the caller is the campaign_owner
@route(campaignBlueprint, '/<campaign_id>', methods=['DELETE'])
def cancel_campaigns(campaign_id):
    return current_app.campaign_controller.cancel_campaign(request, int(campaign_id))


@route(campaignBlueprint, '/<campaign_id>/orders', methods=['GET'])
def get_campaign_orders(campaign_id):
    return current_app.campaign_controller.get_campaign_orders(request, int(campaign_id))


# Pledges
@route(pledgeBlueprint, '/<pledge_id>', methods=['DELETE'])
@validate_bearer_token
def cancel_pledge(pledge_id, user_data):
    return current_app.pledge_controller.cancel_pledge(request, int(pledge_id))


@route(pledgeBlueprint, '/', methods=['GET'])
def get_pledges():
    return current_app.pledge_controller.get_pledges(request)


@route(pledgeBlueprint, '/payment', methods=['POST'])
@validate_bearer_token
def create_pledge_with_payment(user_data):
    return current_app.pledge_controller.create_pledge_with_payment(request, user_data)


# Orders
@route(orderBlueprint, '/status/massive', methods=['PATCH'])
def update_order_statuses():
    return current_app.order_controller.update_order_statuses_massively(request)


@route(orderBlueprint, '/<order_id>', methods=['PATCH'])
def update_order(order_id):
    return current_app.order_controller.update_order(request, int(order_id))


@route(orderBlueprint, '/buyers/<buyer_id>/campaigns/<campaign_id>', methods=['GET'])
def get_campaign_order_from_buyer(buyer_id, campaign_id):
    return current_app.order_controller.get_campaign_order_from_buyer(request, int(buyer_id), int(campaign_id))


# Auth
@route(authBlueprint, '/login', methods=['POST'])
def login():
    api_response, status = current_app.auth_controller.login(request)
    cookie_response = make_response(api_response)
    cookie_response.status = status
    cookie_response.set_cookie(
        key="printmob-backend-cookie",
        value=api_response["token"]
    )

    return cookie_response


@route(authBlueprint, '/signup/validate', methods=['POST'])
def validate_user_data():
    return current_app.auth_controller.validate_user_data(request)


@route(authBlueprint, '/signup/printer', methods=['POST'])
def create_printer():
    return current_app.auth_controller.create_printer(request)


@route(authBlueprint, '/signup/buyer', methods=['POST'])
def create_buyer():
    return current_app.auth_controller.create_buyer(request)


# Users
@route(userBlueprint, '/<user_id>/profile', methods=['GET'])
@validate_bearer_token
def get_user_profile(user_id, user_data):
    return current_app.user_controller.get_user_profile(request, int(user_id), user_data)


@route(userBlueprint, '/<user_id>/balance', methods=['GET'])
@validate_bearer_token
def get_user_balance(user_id, user_data):
    return current_app.user_controller.get_user_balance(request, int(user_id), user_data)


@route(userBlueprint, '/<user_id>/balance', methods=['POST'])
@validate_bearer_token
def request_balance(user_id, user_data):
    return current_app.user_controller.request_balance(request, int(user_id), user_data)


@route(userBlueprint, '/<user_id>/profile', methods=['PUT'])
@validate_bearer_token
def update_user_profile(user_id, user_data):
    return current_app.user_controller.update_user_profile(request, int(user_id), user_data)


# Buyers
@route(buyerBlueprint, '/<buyer_id>/campaigns', methods=['GET'])
def get_buyer_campaigns(buyer_id):
    return current_app.campaign_controller.get_buyer_campaigns(request, int(buyer_id))
