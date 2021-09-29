import datetime

from my_app.api.domain.model import Model
from my_app.api.domain.printer import Printer


class ModelPurchase:
    def __init__(
            self,
            id: int,
            printer: Printer,
            model: Model,
            price: float,
            transaction_id: int,
            created_at: datetime.datetime = datetime.datetime.utcnow(),
    ):
        self.id = id
        self.printer = printer
        self.model = model
        self.price = price
        self.transaction_id = transaction_id
        self.created_at = created_at

    def to_json(self):
        return {
            "id": self.id,
            "printer": self.printer.to_json() if self.printer is not None else None,
            "model": self.model.to_json() if self.model is not None else None,
            "price": self.price,
            "transaction_id": self.transaction_id,
            "created_at": self.created_at,
        }
