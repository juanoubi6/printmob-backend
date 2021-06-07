from my_app.api.repositories.models import PrinterModel


class PrinterRepository:
    def __init__(self, db):
        self.db = db

    def exists_printer(self, printer_id: int) -> bool:
        return self.db.session.query(PrinterModel).filter_by(id=printer_id).first() is not None
