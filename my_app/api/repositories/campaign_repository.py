from datetime import datetime

from sqlalchemy import asc
from sqlalchemy.orm import noload

from my_app.api.domain import Page, Campaign
from my_app.api.domain.campaign import CampaignPrototype
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories.models import CampaignModel, CampaignModelImageModel, UserModel, TechDetailsModel, \
    PrinterModel, BuyerModel
from my_app.api.repositories.utils import paginate, DEFAULT_PAGE, DEFAULT_PAGE_SIZE

CAMPAIGN_NOT_FOUND = 'Non-existent campaign'


class CampaignRepository:
    def __init__(self, db):
        self.db = db

    def init_campaigns(self):
        printer_user_model = UserModel(first_name='Lucas',
                                       last_name='Costas',
                                       user_name='Chikinkun',
                                       date_of_birth=datetime.now(),
                                       email='lcostas@gmail.com')
        self.db.session.add(printer_user_model)
        self.db.session.commit()

        buyer_user_model = UserModel(first_name='Juan',
                                     last_name='Oubina',
                                     user_name='Oubi',
                                     date_of_birth=datetime.now(),
                                     email='oubi@gmail.com')
        self.db.session.add(buyer_user_model)
        self.db.session.commit()

        printer_model = PrinterModel(id=printer_user_model.id)
        self.db.session.add(printer_model)
        self.db.session.commit()

        buyer_model = BuyerModel(id=buyer_user_model.id)
        self.db.session.add(buyer_model)
        self.db.session.commit()

    def create_campaign(self, prototype: CampaignPrototype) -> Campaign:
        campaign_model = CampaignModel(name=prototype.name,
                                       description=prototype.description,
                                       campaign_picture_url=prototype.campaign_picture_url,
                                       printer_id=prototype.printer_id,
                                       pledge_price=prototype.pledge_price,
                                       start_date=prototype.start_date,
                                       end_date=prototype.end_date,
                                       min_pledgers=prototype.min_pledgers,
                                       max_pledgers=prototype.max_pledgers)

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

    def get_campaigns(self, filters) -> Page[Campaign]:
        """
        Returns paginated campaigns using filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        """
        self.init_campaigns()
        query = self.db.session.query(CampaignModel) \
            .options(noload(CampaignModel.tech_detail)) \
            .options(noload(CampaignModel.images)) \
            .order_by(asc(CampaignModel.id))

        campaign_models = paginate(query, filters).all()
        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=list(map(lambda cm: cm.to_campaign_entity(), campaign_models))
        )

    def get_campaign_detail(self, campaign_id) -> Campaign:
        campaign_model = self.db.session.query(CampaignModel).filter_by(id=campaign_id).first()
        if campaign_model is None:
            raise NotFoundException(CAMPAIGN_NOT_FOUND)
        return campaign_model.to_campaign_entity()
