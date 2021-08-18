import os
import threading
import time
from typing import Callable

import schedule

from my_app.api.builder import create_thread_pool_executor, build_ses_client, build_mercadopago_sdk
from my_app.api.db_builder import create_db_session_factory
from my_app.api.repositories import EmailRepository, MercadopagoRepository
from my_app.crons.cancel_campaigns import cancel_campaigns
from my_app.crons.finalize_campaigns import finalize_campaign

db_session_factory = create_db_session_factory(os.environ["DATABASE_URL"])
executor = create_thread_pool_executor()
email_repository = EmailRepository(build_ses_client(), os.environ["SENDER_EMAIL"])
mercadopago_repository = MercadopagoRepository(
    build_mercadopago_sdk(),
    os.environ["PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS"],
    os.environ["PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT"]
)


def run_threaded(cron_func: Callable, params: tuple):
    job_thread = threading.Thread(target=cron_func, args=params)
    job_thread.start()


if __name__ == '__main__':
    # Add your crons here
    schedule.every().day.at("00:00").do(
        run_threaded,
        cron_func=finalize_campaign,
        params=(db_session_factory, email_repository, executor, mercadopago_repository)
    )
    schedule.every().day.at("00:00").do(
        run_threaded,
        cron_func=cancel_campaigns,
        params=(db_session_factory, email_repository, executor, mercadopago_repository)
    )
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)
