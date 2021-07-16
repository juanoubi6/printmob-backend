from concurrent.futures import Executor

from sqlalchemy.orm import sessionmaker

from my_app.api.repositories import EmailRepository
from my_app.crons import finalize_campaign


# This controller is not meant to be used by the frontend. It's just for testing
class CronController:
    def __init__(self,
                 session_factory: sessionmaker,
                 email_repository: EmailRepository,
                 executor: Executor,
                 mercadopago_repository
                 ):
        self.session_factory = session_factory
        self.email_repository = email_repository
        self.executor = executor
        self.mercadopago_repository = mercadopago_repository

    def end_campaigns(self) -> (dict, int):
        self.executor.submit(finalize_campaign, self.session_factory, self.email_repository, self.executor,
                             self.mercadopago_repository)
        return {"result": "executing"}, 200
