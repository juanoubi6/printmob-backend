from flask import Blueprint, current_app, request, make_response

from my_app.api import route
from my_app.api.controllers import validate_bearer_token, get_user_data_if_sent

campaignBlueprint = Blueprint('campaignController', __name__, url_prefix='/campaigns')
buyerBlueprint = Blueprint('buyerBlueprint', __name__, url_prefix='/buyers')
designerBlueprint = Blueprint('designerBlueprint', __name__, url_prefix='/designers')
pledgeBlueprint = Blueprint('pledgeController', __name__, url_prefix='/pledges')
orderBlueprint = Blueprint('orderController', __name__, url_prefix='/orders')
userBlueprint = Blueprint('userController', __name__, url_prefix='/users')
authBlueprint = Blueprint('authController', __name__, url_prefix='/auth')
modelBlueprint = Blueprint('modelController', __name__, url_prefix='/models')
healthBlueprint = Blueprint('healthController', __name__, url_prefix='/health')


# for load balancing purposes
@route(healthBlueprint, '/', methods=['GET'])
def healthy():
    return ''


########################### Testing endpoint ###########################
@route(campaignBlueprint, '/end-campaigns', methods=['POST'])  # Testing-use
def end_campaigns():
    return current_app.cron_controller.end_campaigns()


@route(campaignBlueprint, '/fixture-data', methods=['POST'])  # Testing-use
def fixture_data():
    return current_app.cron_controller.create_test_data(request)


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


@route(campaignBlueprint, '/from-model', methods=['POST'])
@validate_bearer_token
def create_campaign_from_model(user_data):
    return current_app.campaign_controller.create_campaign_from_model(request)


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


@route(orderBlueprint, '/printers/<printer_id>', methods=['GET'])
@validate_bearer_token
def get_orders_of_printer(printer_id, user_data):
    return current_app.order_controller.get_orders_of_printer(request, int(printer_id), user_data)


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


@route(authBlueprint, '/signup/designer', methods=['POST'])
def create_designer():
    return current_app.auth_controller.create_designer(request)


@route(authBlueprint, '/signup/buyer', methods=['POST'])
def create_buyer():
    return current_app.auth_controller.create_buyer(request)


# Users
@route(userBlueprint, '/<user_id>/profile', methods=['GET'])
@validate_bearer_token
def get_user_profile(user_id, user_data):
    return current_app.user_controller.get_user_profile(request, int(user_id), user_data)


@route(userBlueprint, '/<user_id>/data-dashboard', methods=['GET'])
@validate_bearer_token
def get_user_data_dashboard(user_id, user_data):
    return current_app.user_controller.get_user_data_dashboard(request, int(user_id), user_data)


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


# Designers
@route(designerBlueprint, '/<designer_id>/models', methods=['GET'])
@validate_bearer_token
def get_designer_models(designer_id, user_data):
    return current_app.model_controller.get_designer_models(request, int(designer_id), user_data)

@route(designerBlueprint, '/<designer_id>/campaigns', methods=['GET'])
@validate_bearer_token
def get_designer_campaigns(designer_id, user_data):
    return current_app.campaign_controller.get_designer_campaigns(request, int(designer_id), user_data)


# Models
@route(modelBlueprint, '/', methods=['POST'])
@validate_bearer_token
def create_model(user_data):
    return current_app.model_controller.create_model(request, user_data)


@route(modelBlueprint, '/<model_id>/images', methods=['POST'])
@validate_bearer_token
def create_model_image(model_id, user_data):
    return current_app.model_controller.create_model_image(request, int(model_id), user_data)


@route(modelBlueprint, '/<model_id>/images/<model_image_id>', methods=['DELETE'])
@validate_bearer_token
def delete_model_image(model_id, model_image_id, user_data):
    return current_app.model_controller.delete_model_image(
        request,
        int(model_id),
        int(model_image_id),
        user_data
    )


@route(modelBlueprint, '/categories', methods=['GET'])
def get_model_categories():
    return current_app.model_controller.get_model_categories(request)


@route(modelBlueprint, '/ordering', methods=['GET'])
def get_model_ordering():
    return current_app.model_controller.get_model_ordering(request)


@route(modelBlueprint, '/<model_id>/likes', methods=['POST'])
@validate_bearer_token
def add_like_to_model(model_id, user_data):
    return current_app.model_controller.add_like_to_model(request, int(model_id), user_data)


@route(modelBlueprint, '/<model_id>/likes', methods=['DELETE'])
@validate_bearer_token
def remove_like_from_model(model_id, user_data):
    return current_app.model_controller.remove_like_from_model(request, int(model_id), user_data)


@route(modelBlueprint, '/purchases', methods=['POST'])
@validate_bearer_token
def create_model_purchase(user_data):
    return current_app.model_controller.create_model_purchase(request, user_data)


@route(modelBlueprint, '/printers/purchases', methods=['GET'])
@validate_bearer_token
def get_printer_model_purchase(user_data):
    return current_app.model_controller.get_printer_model_purchase(request, user_data)


@route(modelBlueprint, '/<model_id>/purchase', methods=['GET'])
@validate_bearer_token
def get_model_purchase_from_printer(model_id, user_data):
    return current_app.model_controller.get_model_purchase_from_printer(request, int(model_id), user_data)


@route(modelBlueprint, '/<model_id>', methods=['GET'])
@get_user_data_if_sent
def get_model_detail(model_id, user_data):
    return current_app.model_controller.get_model_detail(request, int(model_id), user_data)


@route(modelBlueprint, '/<model_id>/campaigns', methods=['GET'])
def get_model_current_campaigns(model_id):
    return current_app.model_controller.get_model_current_campaigns(request, int(model_id))


@route(modelBlueprint, '/', methods=['GET'])
@get_user_data_if_sent
def get_models(user_data):
    return current_app.model_controller.get_models(request, user_data)


@route(modelBlueprint, '/<model_id>', methods=['DELETE'])
@validate_bearer_token
def delete_model(model_id, user_data):
    return current_app.model_controller.delete_model(request, int(model_id), user_data)


@route(modelBlueprint, '/model-image-data', methods=['GET'])
def get_model_image_data():
    return current_app.model_controller.get_model_image_data(request)
