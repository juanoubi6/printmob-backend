import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import boto3

from my_app.api.controllers import CampaignController, PledgeController, OrderController, AuthController
from my_app.api.repositories import CampaignRepository, PledgeRepository, S3Repository, EmailRepository, \
    GoogleRepository, PrinterRepository, OrderRepository, UserRepository
from my_app.api.services import CampaignService, PledgeService, OrderService, AuthService
from my_app.api.utils.token_manager import TokenManager
from my_app.settings import AWS_BUCKET_NAME, SENDER_EMAIL, GOOGLE_CLIENT_ID, GOOGLE_AUTH_FALLBACK_URL, JWT_SECRET_KEY


def inject_controllers(app, db):
    executor = create_thread_pool_executor()
    s3_client = build_s3_client()
    ses_client = build_ses_client()

    app.campaign_controller = build_campaign_controller(db, s3_client)
    app.pledge_controller = build_pledge_controller(db)
    app.order_controller = build_order_controller(db, executor, ses_client)
    app.auth_controller = build_auth_controller(db, executor)
    app.token_manager = TokenManager(JWT_SECRET_KEY)


def build_campaign_controller(db, s3_client):
    campaign_repository = CampaignRepository(db)
    printer_repository = PrinterRepository(db)
    s3_repository = S3Repository(s3_client, AWS_BUCKET_NAME)

    campaign_service = CampaignService(campaign_repository,
                                       printer_repository,
                                       s3_repository)

    return CampaignController(campaign_service)


def build_pledge_controller(db):
    campaign_repository = CampaignRepository(db)
    pledge_repository = PledgeRepository(db, campaign_repository)
    pledge_service = PledgeService(pledge_repository, campaign_repository)

    return PledgeController(pledge_service)


def build_order_controller(db, executor, ses_client):
    order_repository = OrderRepository(db)
    email_repository = EmailRepository(ses_client, SENDER_EMAIL)
    order_service = OrderService(order_repository, email_repository, executor)

    return OrderController(order_service)


def build_auth_controller(db, executor):
    google_repository = GoogleRepository(GOOGLE_CLIENT_ID, GOOGLE_AUTH_FALLBACK_URL)
    user_repository = UserRepository(db)
    token_manager = TokenManager(JWT_SECRET_KEY)
    auth_service = AuthService(google_repository, user_repository, token_manager)

    executor.submit(google_repository.warm_up)

    return AuthController(auth_service)


def build_s3_client():
    return boto3.client('s3')


def build_ses_client():
    return boto3.client('ses')


def create_thread_pool_executor():
    return ThreadPoolExecutor(
        max_workers=multiprocessing.cpu_count(),
        thread_name_prefix="flask_pool_executor_thread"
    )
