class BankInformation:
    def __init__(
            self,
            id: int,
            cbu: str,
            bank: str,
            account_number: str,
            alias: str = None
    ):
        self.id = id
        self.cbu = cbu
        self.bank = bank
        self.account_number = account_number
        self.alias = alias

    def to_json(self):
        return {
            "id": self.id,
            "cbu": self.cbu,
            "bank": self.bank,
            "account_number": self.account_number,
            "alias": self.alias
        }


class BankInformationPrototype:
    def __init__(
            self,
            cbu: str,
            bank: str,
            account_number: str,
            alias: str = None
    ):
        self.cbu = cbu
        self.bank = bank
        self.account_number = account_number
        self.alias = alias
