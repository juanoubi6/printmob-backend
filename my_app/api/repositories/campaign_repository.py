from datetime import datetime

from sqlalchemy import asc
from sqlalchemy.orm import noload

from my_app.api.domain import Page, Campaign, CampaignModelImagePrototype, CampaignModelImage, CampaignPrototype, \
    CampaignStatus, Order, UserType, OrderStatus
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories.models import CampaignModel, CampaignModelImageModel, UserModel, TechDetailsModel, \
    PrinterModel, BuyerModel, PledgeModel, AddressModel, OrderModel, BankInformationModel
from my_app.api.repositories.utils import paginate, DEFAULT_PAGE, DEFAULT_PAGE_SIZE, apply_campaign_filters

CAMPAIGN_NOT_FOUND = 'Non-existent campaign'
CAMPAIGN_MODEL_IMAGE_NOT_FOUND = 'Non-existent campaign model image'


class CampaignRepository:
    def __init__(self, db):
        self.db = db

    def init_campaigns(self):
        printer_user_model = UserModel(first_name='Juanma',
                                       last_name='Oubina',
                                       user_name='juanmaprinter',
                                       date_of_birth=datetime.now(),
                                       email='juan.manuel.oubina@gmail.com',
                                       user_type=UserType.PRINTER.value)
        self.db.session.add(printer_user_model)
        self.db.session.flush()

        buyer_user_model = UserModel(first_name='Juanma',
                                     last_name='Oubina',
                                     user_name='juanmabuyer',
                                     date_of_birth=datetime.now(),
                                     email='joubina@frba.utn.edu.ar',
                                     user_type=UserType.BUYER.value)
        self.db.session.add(buyer_user_model)
        self.db.session.flush()

        bank_information_model = BankInformationModel(
            cbu="2222222222333333333344",
            alias="Alias",
            bank="Banco galicia",
            account_number="123456-78"
        )
        self.db.session.add(bank_information_model)
        self.db.session.flush()

        printer_model = PrinterModel(id=printer_user_model.id, bank_information_id=bank_information_model.id)
        self.db.session.add(printer_model)
        self.db.session.flush()

        address_model = AddressModel(
            address="Calle falsa 123",
            zip_code="C1425",
            province="CABA",
            city="CABA",
            floor="7",
            apartment="A"
        )
        self.db.session.add(address_model)
        self.db.session.flush()

        buyer_model = BuyerModel(id=buyer_user_model.id, address_id=address_model.id)
        self.db.session.add(buyer_model)
        self.db.session.flush()

        campaign_model = CampaignModel(name='Vaso calavera',
                                       description='Un vaso con forma de calavera',
                                       campaign_picture_url='https://s3.us-east-2.amazonaws.com/printmob-dev/campaign_model_images/default_logo',
                                       printer_id=printer_model.id,
                                       pledge_price=350.0,
                                       end_date=datetime.now(),
                                       min_pledgers=6,
                                       max_pledgers=10,
                                       status=CampaignStatus.IN_PROGRESS.value)
        self.db.session.add(campaign_model)
        self.db.session.flush()

        campaign_model_image = CampaignModelImageModel(
            campaign_id=campaign_model.id,
            model_picture_url="https://s3.us-east-2.amazonaws.com/printmob-dev/campaign_model_images/default_logo",
            file_name="image file name"
        )

        self.db.session.add(campaign_model_image)
        self.db.session.flush()

        pledge_model = PledgeModel(campaign_id=campaign_model.id,
                                   pledge_price=campaign_model.pledge_price,
                                   buyer_id=buyer_model.id)
        self.db.session.add(pledge_model)
        self.db.session.flush()

        tech_detail_model = TechDetailsModel(material="Material",
                                             weight=10,
                                             campaign_id=campaign_model.id,
                                             width=11,
                                             length=12,
                                             depth=13)
        self.db.session.add(tech_detail_model)
        self.db.session.flush()

        order_model = OrderModel(
            campaign_id=campaign_model.id,
            pledge_id=pledge_model.id,
            buyer_id=buyer_model.id,
            status=OrderStatus.IN_PROGRESS.value
        )
        self.db.session.add(order_model)
        self.db.session.commit()

        # More users
        # Axel
        axel_printer_user = UserModel(first_name='Axel',
                                       last_name='Furlan',
                                       user_name='axelprinter',
                                       date_of_birth=datetime.now(),
                                       email='axel.furlan95@gmail.com',
                                       user_type=UserType.PRINTER.value)
        self.db.session.add(axel_printer_user)
        self.db.session.flush()

        axel_printer = PrinterModel(id=axel_printer_user.id, bank_information_id=bank_information_model.id)
        self.db.session.add(axel_printer)
        self.db.session.flush()

        axel_buyer_model = UserModel(first_name='Axel',
                                     last_name='Furlan',
                                     user_name='axelbuyer',
                                     date_of_birth=datetime.now(),
                                     email='afurlanfigueroa@frba.utn.edu.ar',
                                     user_type=UserType.BUYER.value)
        self.db.session.add(axel_buyer_model)
        self.db.session.flush()

        axel_buyer = BuyerModel(id=axel_buyer_model.id, address_id=address_model.id)
        self.db.session.add(axel_buyer)
        self.db.session.flush()

        # Joaco
        joaco_printer_user = UserModel(first_name='Joaquin',
                                       last_name='Leon',
                                       user_name='joacoprinter',
                                       date_of_birth=datetime.now(),
                                       email='leonjoaquin77@gmail.com',
                                       user_type=UserType.PRINTER.value)
        self.db.session.add(joaco_printer_user)
        self.db.session.flush()

        joaco_printer = PrinterModel(id=joaco_printer_user.id, bank_information_id=bank_information_model.id)
        self.db.session.add(joaco_printer)
        self.db.session.flush()

        joaco_buyer_model = UserModel(first_name='Joaquin',
                                     last_name='Leon',
                                     user_name='joacobuyer',
                                     date_of_birth=datetime.now(),
                                     email='jleon@frba.utn.edu.ar',
                                     user_type=UserType.BUYER.value)
        self.db.session.add(joaco_buyer_model)
        self.db.session.flush()

        joaco_buyer = BuyerModel(id=joaco_buyer_model.id, address_id=address_model.id)
        self.db.session.add(joaco_buyer)
        self.db.session.flush()

        # Lucas
        lucas_printer_user = UserModel(first_name='Lucas',
                                       last_name='Costas',
                                       user_name='lucasprinter',
                                       date_of_birth=datetime.now(),
                                       email='lucascostasutn@gmail.com',
                                       user_type=UserType.PRINTER.value)
        self.db.session.add(lucas_printer_user)
        self.db.session.flush()

        lucas_printer = PrinterModel(id=lucas_printer_user.id, bank_information_id=bank_information_model.id)
        self.db.session.add(lucas_printer)
        self.db.session.flush()

        lucas_buyer_model = UserModel(first_name='Lucas',
                                     last_name='Costas',
                                     user_name='lucasbuyer',
                                     date_of_birth=datetime.now(),
                                     email='lucas.costas@mercadolibre.com',
                                     user_type=UserType.BUYER.value)
        self.db.session.add(lucas_buyer_model)
        self.db.session.flush()

        lucas_buyer = BuyerModel(id=lucas_buyer_model.id, address_id=address_model.id)
        self.db.session.add(lucas_buyer)
        self.db.session.flush()

        # Pedro
        pedro_printer_user = UserModel(first_name='Pedro',
                                       last_name='Droven',
                                       user_name='pedroprinter',
                                       date_of_birth=datetime.now(),
                                       email='pdroven@gmail.com',
                                       user_type=UserType.PRINTER.value)
        self.db.session.add(pedro_printer_user)
        self.db.session.flush()

        pedro_printer = PrinterModel(id=pedro_printer_user.id, bank_information_id=bank_information_model.id)
        self.db.session.add(pedro_printer)
        self.db.session.flush()

        pedro_buyer_model = UserModel(first_name='Pedro',
                                     last_name='Droven',
                                     user_name='pedrobuyer',
                                     date_of_birth=datetime.now(),
                                     email='pdroven@frba.utn.edu.ar',
                                     user_type=UserType.BUYER.value)
        self.db.session.add(pedro_buyer_model)
        self.db.session.flush()

        pedro_buyer = BuyerModel(id=pedro_buyer_model.id, address_id=address_model.id)
        self.db.session.add(pedro_buyer)
        self.db.session.flush()
        self.db.session.commit()

    def create_campaign(self, prototype: CampaignPrototype) -> Campaign:
        campaign_model = CampaignModel(name=prototype.name,
                                       description=prototype.description,
                                       campaign_picture_url=prototype.campaign_picture_url,
                                       printer_id=prototype.printer_id,
                                       pledge_price=prototype.pledge_price,
                                       end_date=prototype.end_date,
                                       min_pledgers=prototype.min_pledgers,
                                       max_pledgers=prototype.max_pledgers,
                                       status=prototype.status.value)

        tech_detail_model = TechDetailsModel(material=prototype.tech_details.material,
                                             weight=prototype.tech_details.weight,
                                             width=prototype.tech_details.width,
                                             length=prototype.tech_details.length,
                                             depth=prototype.tech_details.depth)

        self.db.session.add(campaign_model)
        self.db.session.flush()

        tech_detail_model.campaign_id = campaign_model.id
        self.db.session.add(tech_detail_model)

        self.db.session.commit()

        return campaign_model.to_campaign_entity()

    def get_campaigns(self, filters: dict) -> Page[Campaign]:
        """
        Returns paginated campaigns using filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        """
        query = self.db.session.query(CampaignModel).filter(CampaignModel.deleted_at == None)
        query = apply_campaign_filters(query, filters)
        query = query.options(noload(CampaignModel.tech_detail)).order_by(asc(CampaignModel.id))

        campaign_models = paginate(query, filters).all()

        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=[cm.to_campaign_entity() for cm in campaign_models]
        )

    def get_campaign_detail(self, campaign_id: int) -> Campaign:
        return self._get_campaign_model_by_id(campaign_id).to_campaign_entity()

    def change_campaign_status(self, campaign_id: int, new_status: CampaignStatus):
        campaign_model = self._get_campaign_model_by_id(campaign_id)
        campaign_model.status = new_status.value
        self.db.session.commit()

    def create_campaign_model_image(self, prototype: CampaignModelImagePrototype) -> CampaignModelImage:
        campaign_model_image_model = CampaignModelImageModel(
            campaign_id=prototype.campaign_id,
            model_picture_url=prototype.model_picture_url,
            file_name=prototype.file_name
        )

        self.db.session.add(campaign_model_image_model)
        self.db.session.commit()

        return campaign_model_image_model.to_campaign_model_image_entity()

    def delete_campaign_model_image(self, campaign_model_image_id: int) -> CampaignModelImage:
        campaign_model_image_model = self.db.session.query(CampaignModelImageModel) \
            .filter_by(id=campaign_model_image_id) \
            .first()
        if campaign_model_image_model is None:
            raise NotFoundException(CAMPAIGN_MODEL_IMAGE_NOT_FOUND)

        self.db.session.delete(campaign_model_image_model)
        self.db.session.commit()

        return campaign_model_image_model.to_campaign_model_image_entity()

    def get_campaign_orders(self, campaign_id: int, filters: dict) -> Page[Order]:
        """
        Returns paginated orders of a campaign using filters

        Parameters
        ----------
        campaign_id: int
            Campaign id reference.
        filters: dict[str,str]
            Dict with filters to apply.
        """
        query = self.db.session.query(OrderModel) \
            .filter(OrderModel.campaign_id == campaign_id) \
            .order_by(asc(OrderModel.id))

        order_models = paginate(query, filters).all()
        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=[om.to_order_entity() for om in order_models]
        )

    def get_buyer_campaigns(self, buyer_id: int, filters: dict) -> Page[Campaign]:
        """
        Returns paginated buyer campaigns using filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        buyer_id: int
            Buyer id.
        """
        query = self.db.session.query(CampaignModel).join(PledgeModel)\
            .filter(CampaignModel.id == PledgeModel.campaign_id)\
            .filter(PledgeModel.buyer_id == buyer_id)\
            .filter(PledgeModel.deleted_at == None)\
            .options(noload(CampaignModel.tech_detail)) \
            .order_by(asc(CampaignModel.id))

        campaign_models = paginate(query, filters).all()

        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=[cm.to_campaign_entity() for cm in campaign_models]
        )

    def _get_campaign_model_by_id(self, campaign_id: int) -> CampaignModel:
        campaign_model = self.db.session.query(CampaignModel) \
            .filter_by(id=campaign_id) \
            .filter(CampaignModel.deleted_at == None) \
            .first()

        if campaign_model is None:
            raise NotFoundException(CAMPAIGN_NOT_FOUND)

        return campaign_model
