from datetime import datetime

from sqlalchemy import asc, null
from sqlalchemy.orm import noload

from my_app.api.domain import Page, Campaign
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories.models import CampaignModel, CampaignModelImageModel, UserModel, PledgeModel, \
    TechDetailsModel, \
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

        campaign_model = CampaignModel(name='Vaso calavera',
                                       description='Un vaso con forma de calavera',
                                       campaign_picture_url='https://free3d.com/imgd/l80/1089780.jpg',
                                       printer_id=printer_model.id,
                                       pledge_price=350.0,
                                       start_date=datetime.strptime("21 May, 2021", "%d %B, %Y"),
                                       end_date=datetime.now(),
                                       min_pledgers=6,
                                       max_pledgers=10)
        self.db.session.add(campaign_model)
        self.db.session.commit()

        tech_detail = TechDetailsModel(campaign_id=campaign_model.id,
                                       material='PLA',
                                       weight=80,
                                       width=80,
                                       length=80,
                                       depth=78)
        self.db.session.add(tech_detail)
        self.db.session.commit()

        first_pledge = PledgeModel(campaign_id=campaign_model.id,
                                   pledge_price=350.0,
                                   buyer_id=buyer_model.id)
        self.db.session.add(first_pledge)
        self.db.session.commit()

        model_image = CampaignModelImageModel(campaign_id=campaign_model.id,
                                              model_picture_url="https://free3d.com/imgd/l80/1089780.jpg")
        self.db.session.add(model_image)
        self.db.session.commit()

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
            .filter(CampaignModel.deleted_at is null)\
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
        campaign_model = self.db.session.query(CampaignModel)\
            .filter_by(id=campaign_id)\
            .filter(CampaignModel.deleted_at is null) \
            .first()
        if campaign_model is None:
            raise NotFoundException(CAMPAIGN_NOT_FOUND)
        return campaign_model.to_campaign_entity()
