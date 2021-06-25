import os
import threading
import time
from typing import Callable

import schedule

from my_app.api.builder import create_thread_pool_executor, build_ses_client
from my_app.api.db_builder import create_db_session_factory
from my_app.api.repositories import EmailRepository
from my_app.crons.finalize_campaigns import finalize_campaign

db_session_factory = create_db_session_factory(os.environ["DATABASE_URL"])
executor = create_thread_pool_executor()
email_repository = EmailRepository(build_ses_client(), os.environ["SENDER_EMAIL"])


def run_threaded(cron_func: Callable, params: tuple):
    job_thread = threading.Thread(target=cron_func, args=params)
    job_thread.start()


if __name__ == '__main__':
    # Add your crons here
    schedule.every().day.at("00:00").do(
        run_threaded,
        cron_func=finalize_campaign,
        params=(db_session_factory, email_repository, executor, "mercadopagoRepository")
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
