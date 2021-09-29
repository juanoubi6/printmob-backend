import datetime

from sqlalchemy import func

from my_app.api.domain import Balance
from my_app.api.repositories.models import TransactionModel, BalanceRequestModel

PLEDGE_TRANSACTION_ASSOCIATION_ERROR = "Ocurrió un error al crear la transacción asociada a la reserva"


class TransactionRepository:
    def __init__(self, db):
        self.db = db

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

    def create_balance_request(self, user_id: int) -> (float, bool):
        send_email = False

        current_balance = self.db.session.query(
            func.sum(TransactionModel.amount).label("current_balance")
        ).filter(TransactionModel.user_id == user_id).filter(TransactionModel.is_future == False).first()

        balance = 0.0 if current_balance[0] is None else float(current_balance[0])

        if int(balance) != 0:
            # Update existing request date
            existing_balance_request = self.db.session.query(BalanceRequestModel).filter_by(user_id=user_id).first()

            if existing_balance_request is None:
                balance_request_model = BalanceRequestModel(
                    user_id=user_id,
                    date=datetime.datetime.now()
                )
                self.db.session.add(balance_request_model)
                send_email = True
            else:
                existing_balance_request.date = datetime.datetime.now()

            self.db.session.commit()

        return balance, send_email
