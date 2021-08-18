import datetime

from sqlalchemy import func

from my_app.api.domain import Pledge, TransactionPrototype, Balance
from my_app.api.exceptions import BusinessException
from my_app.api.repositories.models import TransactionModel, BalanceRequestModel
from my_app.api.repositories.pledge_repository import PledgeRepository

PLEDGE_TRANSACTION_ASSOCIATION_ERROR = "Pledge transaction could not be created"


class TransactionRepository:
    def __init__(self, db, pledge_repository: PledgeRepository):
        self.db = db
        self._pledge_repository = pledge_repository

    # TODO: add designer transaction in the future
    def associate_transactions_to_pledge(
            self,
            pledge_id: int,
            printer_transaction_prototype: TransactionPrototype
    ) -> Pledge:
        pledge_model = self._pledge_repository.get_pledge_model_by_id(pledge_id)
        campaign = self._pledge_repository.get_pledge_campaign(pledge_id)

        try:
            printer_transaction_model = TransactionModel(
                mp_payment_id=printer_transaction_prototype.mp_payment_id,
                user_id=campaign.printer.id,
                amount=printer_transaction_prototype.amount,
                type=printer_transaction_prototype.type.value,
                is_future=printer_transaction_prototype.is_future,
            )
            self.db.session.add(printer_transaction_model)
            self.db.session.flush()

            pledge_model.printer_transaction_id = printer_transaction_model.id

            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            pledge_model.deleted_at = datetime.datetime.now()
            self.db.session.commit()
            #Todo: refund pledge?
            raise BusinessException("{}: {}".format(PLEDGE_TRANSACTION_ASSOCIATION_ERROR, str(ex)))

        return pledge_model.to_pledge_entity()

    def get_user_balance(self, user_id: int) -> Balance:
        current_balance = self.db.session.query(
            func.sum(TransactionModel.amount).label("current_balance")
        ).filter(TransactionModel.user_id == user_id).filter(TransactionModel.is_future == False).first()

        future_balance = self.db.session.query(
            func.sum(TransactionModel.amount).label("current_balance")
        ).filter(TransactionModel.user_id == user_id).filter(TransactionModel.is_future == True).first()

        return Balance(
            current_balance=0 if current_balance[0] is None else float(current_balance[0]),
            future_balance=0 if future_balance[0] is None else float(future_balance[0])
        )

    def create_balance_request(self, user_id: int) -> float:
        current_balance = self.db.session.query(
            func.sum(TransactionModel.amount).label("current_balance")
        ).filter(TransactionModel.user_id == user_id).filter(TransactionModel.is_future == False).first()

        balance = 0.0 if current_balance[0] is None else float(current_balance[0])

        if int(balance) != 0:
            balance_request_model = BalanceRequestModel(
                user_id=user_id,
                date=datetime.datetime.now()
            )
            self.db.session.add(balance_request_model)
            self.db.session.commit()

        return balance
