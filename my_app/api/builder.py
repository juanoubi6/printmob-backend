import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import boto3
import mercadopago

from my_app.api.controllers import CampaignController, PledgeController, OrderController, AuthController, \
    CronController, UserController
from my_app.api.db_builder import create_db_session_factory
from my_app.api.repositories import CampaignRepository, PledgeRepository, S3Repository, EmailRepository, \
    GoogleRepository, PrinterRepository, OrderRepository, UserRepository, MercadopagoRepository, TransactionRepository
from my_app.api.services import CampaignService, PledgeService, OrderService, AuthService, UserService
from my_app.api.utils.token_manager import TokenManager
from my_app.settings import AWS_BUCKET_NAME, SENDER_EMAIL, GOOGLE_CLIENT_ID, GOOGLE_AUTH_FALLBACK_URL, JWT_SECRET_KEY, \
    ENV, DB_CONFIG, MERCADOPAGO_ACCESS_TOKEN, PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS, \
    PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT


def inject_controllers(app, db):
    executor = create_thread_pool_executor()
    s3_client = build_s3_client()
    ses_client = build_ses_client()
    mercadopago_sdk = build_mercadopago_sdk()

    # Build repositories
    mercadopago_repository = MercadopagoRepository(mercadopago_sdk, PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS,
                                                   PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT)
    campaign_repository = CampaignRepository(db, mercadopago_repository)
    printer_repository = PrinterRepository(db)
    pledge_repository = PledgeRepository(db, campaign_repository, mercadopago_repository)
    transaction_repository = TransactionRepository(db)
    s3_repository = S3Repository(s3_client, AWS_BUCKET_NAME)
    order_repository = OrderRepository(db)
    email_repository = EmailRepository(ses_client, SENDER_EMAIL)
    google_repository = GoogleRepository(GOOGLE_CLIENT_ID, GOOGLE_AUTH_FALLBACK_URL, executor)
    user_repository = UserRepository(db)

    app.campaign_controller = build_campaign_controller(campaign_repository, printer_repository, s3_repository)
    app.pledge_controller = build_pledge_controller(pledge_repository, campaign_repository, mercadopago_repository)
    app.order_controller = build_order_controller(order_repository, campaign_repository, email_repository, executor)
    app.auth_controller = build_auth_controller(google_repository, user_repository, transaction_repository, executor,
                                                email_repository)
    app.user_controller = build_user_controller(user_repository, transaction_repository, email_repository, executor)
    app.token_manager = TokenManager(JWT_SECRET_KEY)

    # Test-controller
    db_session_factory = create_db_session_factory(DB_CONFIG["SQLALCHEMY_DATABASE_URI"])
    email_repository = EmailRepository(build_ses_client(), SENDER_EMAIL)
    app.cron_controller = CronController(db_session_factory, email_repository, executor, "mercadopago_repo")


def build_campaign_controller(campaign_repository, printer_repository, s3_repository):
    campaign_service = CampaignService(campaign_repository,
                                       printer_repository,
                                       s3_repository)

    return CampaignController(campaign_service)


def build_pledge_controller(pledge_repository, campaign_repository, mercadopago_repository):
    pledge_service = PledgeService(
        pledge_repository, campaign_repository, mercadopago_repository
    )

    return PledgeController(pledge_service)


def build_order_controller(order_repository, campaign_repository, email_repository, executor):
    order_service = OrderService(order_repository, campaign_repository, email_repository, executor)

    return OrderController(order_service)


def build_auth_controller(google_repository, user_repository, transaction_repository, executor, email_repository):
    token_manager = TokenManager(JWT_SECRET_KEY)
    auth_service = AuthService(google_repository, user_repository, token_manager)
    user_service = UserService(user_repository, transaction_repository, email_repository, executor)

    if ENV != "testing":
        executor.submit(google_repository.warm_up)

    return AuthController(auth_service, user_service)


def build_user_controller(user_repository, transaction_repository, email_repository, executor):
    user_service = UserService(user_repository, transaction_repository, email_repository, executor)

    return UserController(user_service)


def build_s3_client():
    return boto3.client('s3')


def build_ses_client():
    return boto3.client('ses')


def create_thread_pool_executor():
    return ThreadPoolExecutor(
        max_workers=multiprocessing.cpu_count(),
        thread_name_prefix="flask_pool_executor_thread"
    )


def build_mercadopago_sdk():
    return mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
