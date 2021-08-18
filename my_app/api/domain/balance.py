class Balance:
    def __init__(
            self,
            current_balance: float,
            future_balance: float
    ):
        self.current_balance = current_balance
        self.future_balance = future_balance

    def to_json(self):
        return {
            "current_balance": self.current_balance,
            "future_balance": self.future_balance
        }
