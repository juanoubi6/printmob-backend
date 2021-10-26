from datetime import datetime

from sqlalchemy import asc, or_, and_
from sqlalchemy.orm import noload

from my_app.api.domain import Page, Campaign, CampaignModelImagePrototype, CampaignModelImage, CampaignPrototype, \
    CampaignStatus, Order, UserType, OrderStatus, TransactionType, CampaignWithModelPrototype
from my_app.api.exceptions import NotFoundException, MercadopagoException, CampaignCreationException
from my_app.api.repositories.mercadopago_repository import MercadopagoRepository
from my_app.api.repositories.models import CampaignModel, CampaignModelImageModel, UserModel, TechDetailsModel, \
    PrinterModel, BuyerModel, PledgeModel, AddressModel, OrderModel, BankInformationModel, TransactionModel, ModelModel
from my_app.api.repositories.utils import paginate, DEFAULT_PAGE, DEFAULT_PAGE_SIZE, apply_campaign_filters, \
    apply_campaign_order_filters

CAMPAIGN_NOT_FOUND = 'La campaña no existe'
CAMPAIGN_MODEL_IMAGE_NOT_FOUND = 'La imagen del modelo de la campaña no existe'
CAMPAIGN_CREATION_ERROR = 'Ocurrió un error al crear la campaña'


class CampaignRepository:
    def __init__(self, db, mercadopago_repository: MercadopagoRepository):
        self.db = db
        self.mercadopago_repository = mercadopago_repository

    def create_campaign(self, prototype: CampaignPrototype) -> Campaign:
        try:
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

            # Create campaign pledge preference
            preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
                campaign_model.to_campaign_entity()
            )

            campaign_model.mp_preference_id = preference_id
            self.db.session.commit()

        except MercadopagoException as mpex:
            self.db.session.rollback()
            raise mpex
        except Exception as ex:
            self.db.session.rollback()
            raise CampaignCreationException("{}: {}".format(CAMPAIGN_CREATION_ERROR, str(ex)))

        return campaign_model.to_campaign_entity()

    def create_campaign_from_model(self, prototype: CampaignWithModelPrototype) -> Campaign:
        try:
            campaign_model = CampaignModel(name=prototype.name,
                                           description=prototype.description,
                                           campaign_picture_url=None,
                                           printer_id=prototype.printer_id,
                                           pledge_price=prototype.pledge_price,
                                           end_date=prototype.end_date,
                                           min_pledgers=prototype.min_pledgers,
                                           max_pledgers=prototype.max_pledgers,
                                           status=prototype.status.value,
                                           model_id=prototype.model_id)

            tech_detail_model = TechDetailsModel(material=prototype.tech_details.material,
                                                 weight=prototype.tech_details.weight,
                                                 width=prototype.tech_details.width,
                                                 length=prototype.tech_details.length,
                                                 depth=prototype.tech_details.depth)

            self.db.session.add(campaign_model)
            self.db.session.flush()

            tech_detail_model.campaign_id = campaign_model.id
            self.db.session.add(tech_detail_model)

            # Get model for campaign
            model_model = self.db.session.query(ModelModel).filter(ModelModel.id == prototype.model_id).first()
            campaign_model.model = model_model

            # Create campaign pledge preference
            preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
                campaign_model.to_campaign_entity()
            )

            campaign_model.mp_preference_id = preference_id

            # Create campaign pictures
            campaign_model_images = [
                CampaignModelImageModel(
                    model_picture_url=model_image.model_picture_url,
                    file_name=model_image.file_name,
                    campaign_id=campaign_model.id
                ) for model_image in prototype.campaign_model_images
            ]
            self.db.session.add_all(campaign_model_images)

            self.db.session.commit()

        except MercadopagoException as mpex:
            self.db.session.rollback()
            raise mpex
        except Exception as ex:
            self.db.session.rollback()
            raise CampaignCreationException("{}: {}".format(CAMPAIGN_CREATION_ERROR, str(ex)))

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
        return self.get_campaign_model_by_id(campaign_id).to_campaign_entity()

    def change_campaign_status(self, campaign_id: int, new_status: CampaignStatus):
        campaign_model = self.get_campaign_model_by_id(campaign_id)
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
        query = self.db.session.query(OrderModel).filter(OrderModel.campaign_id == campaign_id)
        query = apply_campaign_order_filters(query, filters)
        query = query.options(noload(OrderModel.campaign))
        query = query.order_by(asc(OrderModel.id))

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
        active_campaign_filter = and_(
            CampaignModel.status.in_([CampaignStatus.IN_PROGRESS.value, CampaignStatus.CONFIRMED.value, CampaignStatus.TO_BE_FINALIZED.value, CampaignStatus.COMPLETED.value]),
            PledgeModel.deleted_at == None
        )

        closed_campaign_filter = and_(
            CampaignModel.status.in_([CampaignStatus.CANCELLED.value, CampaignStatus.TO_BE_CANCELLED.value, CampaignStatus.UNSATISFIED.value]),
        )

        query = self.db.session.query(CampaignModel).join(PledgeModel).distinct(CampaignModel.id) \
            .filter(CampaignModel.id == PledgeModel.campaign_id)\
            .filter(PledgeModel.buyer_id == buyer_id)\
            .filter(or_(active_campaign_filter, closed_campaign_filter))
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

    def get_designer_campaigns(self, designer_id: int, filters: dict) -> Page[Campaign]:
        """
        Returns paginated designer campaigns using filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        buyer_id: int
            Buyer id.
        """
        query = self.db.session.query(CampaignModel).join(ModelModel)\
            .filter(ModelModel.id == CampaignModel.model_id)\
            .filter(ModelModel.designer_id == designer_id)
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

    def get_campaign_model_by_id(self, campaign_id: int) -> CampaignModel:
        campaign_model = self.db.session.query(CampaignModel) \
            .filter_by(id=campaign_id) \
            .filter(CampaignModel.deleted_at == None) \
            .first()

        if campaign_model is None:
            raise NotFoundException(CAMPAIGN_NOT_FOUND)

        return campaign_model
