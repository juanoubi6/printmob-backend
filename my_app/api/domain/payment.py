class Payment:
    def __init__(
            self,
            payment_id: int,
            payment_data: dict
    ):
        self.payment_id = payment_id
        self._payment_data = payment_data

    def get_transaction_net_amount(self):
        return self._payment_data["transaction_details"]["net_received_amount"]
