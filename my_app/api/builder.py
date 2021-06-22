import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import boto3

from my_app.api.controllers import CampaignController, PledgeController
from my_app.api.repositories import CampaignRepository, PledgeRepository, S3Repository
from my_app.api.repositories.printer_repository import PrinterRepository
from my_app.api.services import CampaignService, PledgeService
from my_app.settings import AWS_BUCKET_NAME


def inject_controllers(app, db):
    s3_client = build_s3_client()

    app.campaign_controller = build_campaign_controller(db, s3_client)
    app.pledge_controller = build_pledge_controller(db)


def build_campaign_controller(db, s3_client):
    campaign_repository = CampaignRepository(db)
    printer_repository = PrinterRepository(db)
    s3_repository = S3Repository(s3_client, AWS_BUCKET_NAME)

    campaign_service = CampaignService(campaign_repository,
                                       printer_repository,
                                       s3_repository)

    return CampaignController(campaign_service)


def build_pledge_controller(db):
    pledge_repository = PledgeRepository(db)
    campaign_repository = CampaignRepository(db)
    pledge_service = PledgeService(pledge_repository, campaign_repository)

    return PledgeController(pledge_service)


def build_s3_client():
    return boto3.client(
        's3'
    )


def create_thread_pool_executor():
    return ThreadPoolExecutor(
        max_workers=multiprocessing.cpu_count(),
        thread_name_prefix="flask_pool_executor_thread"
    )
