import enum


class TransactionType(enum.Enum):
    PLEDGE = "Pledge"
    MODEL_PURCHASE = "Model purchase"
    CASHOUT = "Cashout"
    REFUND = "Refund"


class Transaction:
    def __init__(
            self,
            id: int,
            mp_payment_id: int,
            user_id: int,
            amount: float,
            type: TransactionType,
            is_future: bool
    ):
        self.id = id
        self.mp_payment_id = mp_payment_id
        self.user_id = user_id
        self.amount = amount
        self.type = type
        self.is_future = is_future


class TransactionPrototype:
    def __init__(
            self,
            mp_payment_id: int,
            user_id: int,
            amount: float,
            type: TransactionType,
            is_future: bool
    ):
        self.mp_payment_id = mp_payment_id
        self.user_id = user_id
        self.amount = amount
        self.type = type
        self.is_future = is_future
