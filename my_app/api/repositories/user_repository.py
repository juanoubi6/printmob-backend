import datetime

from sqlalchemy.orm import noload

from my_app.api.domain import Printer, Buyer, User, BuyerPrototype, PrinterPrototype, UserPrototype, CampaignStatus, \
    OrderStatus, PrinterDataDashboard, EndingCampaignResume
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import TransactionRepository
from my_app.api.repositories.models import PrinterModel, UserModel, BuyerModel, AddressModel, BankInformationModel, \
    CampaignModel, OrderModel


class UserRepository:
    def __init__(self, db, transaction_repository: TransactionRepository):
        self.db = db
        self.transaction_repository = transaction_repository

    def get_printer_data_dashboard(self, printer_id: int) -> PrinterDataDashboard:
        # Total amount of in progress and completed campaigns, and the total of current pledges
        current_printer_campaigns = self.db.session.query(CampaignModel) \
            .filter(CampaignModel.printer_id == printer_id) \
            .filter(CampaignModel.deleted_at == None) \
            .filter(CampaignModel.status.in_([CampaignStatus.IN_PROGRESS.value, CampaignStatus.CONFIRMED.value, CampaignStatus.COMPLETED.value])) \
            .options(noload(CampaignModel.tech_detail)) \
            .options(noload(CampaignModel.tech_detail)) \
            .options(noload(CampaignModel.printer)) \
            .options(noload(CampaignModel.images)) \
            .all()

        ending_campaigns = []
        completed_campaign_ids = []
        campaigns_in_progress = 0
        completed_campaigns = 0
        current_pledges = 0

        for campaign in current_printer_campaigns:
            if campaign.status in [CampaignStatus.IN_PROGRESS.value, CampaignStatus.CONFIRMED.value]:
                campaigns_in_progress += 1
                current_pledges += len(campaign.pledges)

                if (campaign.end_date - datetime.datetime.now()).days <= 4:
                    ending_campaigns.append(campaign)
            else:
                completed_campaigns += 1
                completed_campaign_ids.append(campaign.id)

        # Current and future balance
        user_balance = self.transaction_repository.get_user_balance(printer_id)

        # Total pending orders of printer
        in_progress_orders_from_printer = self.db.session.query(OrderModel) \
            .filter(OrderModel.campaign_id.in_(completed_campaign_ids)) \
            .filter(OrderModel.status == OrderStatus.IN_PROGRESS.value) \
            .options(noload(OrderModel.buyer)) \
            .options(noload(OrderModel.campaign)) \
            .all()
        pending_orders = len(in_progress_orders_from_printer) if in_progress_orders_from_printer is not None else 0

        return PrinterDataDashboard(
            campaigns_in_progress=campaigns_in_progress,
            completed_campaigns=completed_campaigns,
            pledges_in_progress=current_pledges,
            balance=user_balance,
            pending_orders=pending_orders,
            ending_campaigns=[self._campaign_model_to_ending_campaign_resume(ec) for ec in ending_campaigns]
        )

    def get_printer_by_email(self, email: str) -> Printer:
        user_model = self._get_user_model_by_email(email)

        return user_model.printer.to_printer_entity()

    def get_buyer_by_email(self, email: str) -> Buyer:
        user_model = self._get_user_model_by_email(email)

        return user_model.buyer.to_buyer_entity() if user_model is not None else None

    def get_user_by_email(self, email: str) -> User:
        user_model = self._get_user_model_by_email(email)

        return user_model.to_user_entity() if user_model is not None else None

    def get_user_by_id(self, id: int) -> User:
        user_model = self._get_user_model_by_id(id)

        return user_model.to_user_entity() if user_model is not None else None

    def is_user_name_in_use(self, user_name: str) -> bool:
        return self.db.session.query(UserModel).filter_by(user_name=user_name.lower()).first() is not None

    def is_email_in_use(self, email: str) -> bool:
        return self.db.session.query(UserModel).filter_by(email=email.lower()).first() is not None

    def create_buyer(self, prototype: BuyerPrototype) -> Buyer:
        user_model = self._create_user_model(prototype.user_prototype)
        self.db.session.add(user_model)

        address_model = AddressModel(
            address=prototype.address_prototype.address,
            zip_code=prototype.address_prototype.zip_code,
            province=prototype.address_prototype.province,
            city=prototype.address_prototype.city,
            floor=prototype.address_prototype.floor,
            apartment=prototype.address_prototype.apartment
        )
        self.db.session.add(address_model)
        self.db.session.flush()

        buyer_model = BuyerModel(id=user_model.id, address_id=address_model.id)
        self.db.session.add(buyer_model)
        self.db.session.commit()

        return buyer_model.to_buyer_entity()

    def update_buyer(self, buyer_id: int, prototype: BuyerPrototype) -> Buyer:
        buyer_model = self._get_buyer_model_by_id(buyer_id)
        if buyer_model is None:
            raise NotFoundException("No se encontró al usuario Comprador")

        buyer_model.user.first_name = prototype.user_prototype.first_name
        buyer_model.user.last_name = prototype.user_prototype.last_name
        buyer_model.user.date_of_birth = prototype.user_prototype.date_of_birth
        buyer_model.user.updated_at = datetime.datetime.now()

        buyer_model.address.address = prototype.address_prototype.address
        buyer_model.address.zip_code = prototype.address_prototype.zip_code
        buyer_model.address.province = prototype.address_prototype.province
        buyer_model.address.city = prototype.address_prototype.city
        buyer_model.address.floor = prototype.address_prototype.floor
        buyer_model.address.apartment = prototype.address_prototype.apartment

        self.db.session.commit()

        return buyer_model.to_buyer_entity()

    def create_printer(self, prototype: PrinterPrototype) -> Printer:
        user_model = self._create_user_model(prototype.user_prototype)
        self.db.session.add(user_model)

        bank_information_model = BankInformationModel(
            cbu=prototype.bank_information_prototype.cbu,
            alias=prototype.bank_information_prototype.alias,
            bank=prototype.bank_information_prototype.bank,
            account_number=prototype.bank_information_prototype.account_number,
        )
        self.db.session.add(bank_information_model)
        self.db.session.flush()

        printer_model = PrinterModel(id=user_model.id, bank_information_id=bank_information_model.id)
        self.db.session.add(printer_model)
        self.db.session.commit()

        return printer_model.to_printer_entity()

    def update_printer(self, printer_id: int, prototype: PrinterPrototype) -> Printer:
        printer_model = self._get_printer_model_by_id(printer_id)
        if printer_model is None:
            raise NotFoundException("No se encontró al usuario Impresor")

        printer_model.user.first_name = prototype.user_prototype.first_name
        printer_model.user.last_name = prototype.user_prototype.last_name
        printer_model.user.date_of_birth = prototype.user_prototype.date_of_birth
        printer_model.user.updated_at = datetime.datetime.now()

        printer_model.bank_information.cbu = prototype.bank_information_prototype.cbu
        printer_model.bank_information.alias = prototype.bank_information_prototype.alias
        printer_model.bank_information.bank = prototype.bank_information_prototype.bank
        printer_model.bank_information.account_number = prototype.bank_information_prototype.account_number

        self.db.session.commit()

        return printer_model.to_printer_entity()

    def _create_user_model(self, prototype: UserPrototype) -> UserModel:
        user_model = UserModel(
            first_name=prototype.first_name,
            last_name=prototype.last_name,
            user_name=prototype.user_name,
            date_of_birth=prototype.date_of_birth,
            email=prototype.email,
            user_type=prototype.user_type.value,
            profile_picture_url=prototype.profile_picture_url
        )

        return user_model

    def _get_user_model_by_email(self, email: str) -> UserModel:
        return self.db.session.query(UserModel).filter_by(email=email).first()

    def _get_user_model_by_id(self, id: int) -> UserModel:
        return self.db.session.query(UserModel).filter_by(id=id).first()

    def _get_buyer_model_by_id(self, user_id: int) -> BuyerModel:
        return self.db.session.query(BuyerModel).filter_by(id=user_id).first()

    def _get_printer_model_by_id(self, user_id: int) -> PrinterModel:
        return self.db.session.query(PrinterModel).filter_by(id=user_id).first()

    def _campaign_model_to_ending_campaign_resume(self, campaign_model: CampaignModel) -> EndingCampaignResume:
        base_percentage = len(campaign_model.pledges) / campaign_model.min_pledgers
        percentage = 100 if base_percentage > 1 else int(base_percentage * 100)

        return EndingCampaignResume(
            id=campaign_model.id,
            name=campaign_model.name,
            percentage=percentage,
            end_date=campaign_model.end_date,
        )
