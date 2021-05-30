from datetime import datetime
from sqlalchemy import desc, func, DateTime

from my_app.api.domain import Campaign
from my_app.api.domain.campaign_detail import CampaignDetail
from my_app.api.repositories.models import CampaignModel, ModelImageModel, UserModel, PledgeModel, TechDetailsModel, \
    PrinterModel, BuyerModel


class CampaignRepository:
    def __init__(self, db):
        self.db = db

    def init_campaigns(self):
        user_model = UserModel(first_name='Lucas',
                               last_name='Costas',
                               user_name='Chikinkun',
                               date_of_birth=datetime.now(),
                               email='lcostas@gmail.com')
        self.db.session.add(user_model)
        self.db.session.commit()

        printer_model = PrinterModel(id=user_model.id)
        self.db.session.add(printer_model)
        self.db.session.commit()

        buyer_model = BuyerModel(id=user_model.id)
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
                                   buyer_id=user_model.id,
                                   pledge_date=datetime.now())
        self.db.session.add(first_pledge)
        self.db.session.commit()

        model_image = ModelImageModel(campaign_id=campaign_model.id,
                                      model_picture_url="https://free3d.com/imgd/l80/1089780.jpg")
        self.db.session.add(model_image)
        self.db.session.commit()

    def get_campaigns(self):
        self.init_campaigns()
        campaign_model = self.db.session.query(CampaignModel).order_by(desc(CampaignModel.id)).first()
        return [Campaign(campaign_model.name, campaign_model.id)]

    def get_campaign_detail(self, campaign_id):
        campaign_model = self.db.session.query(CampaignModel).filter_by(id=campaign_id).first()
        alt_model_pictures_url = self.db.session.query(ModelImageModel.model_picture_url)\
            .filter_by(campaign_id=campaign_id).all()
        printer = self.db.session.query(UserModel).filter_by(id=campaign_model.printer_id).first()
        current_pledgers = self.db.session.query(PledgeModel).filter_by(campaign_id=campaign_id).count()
        tech_details = self.db.session.query(TechDetailsModel).filter_by(campaign_id=campaign_id).first()
        return CampaignDetail(campaign_model, alt_model_pictures_url, printer, current_pledgers, tech_details)
