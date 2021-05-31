from flask import jsonify

from my_app.api.domain.tech_detail import TechDetail
from my_app.api.domain.user import User


class CampaignDetail:
    def __init__(self, campaign_model):  # alt_model_pictures_url, printer_model, current_pledgers, tech_details_model):
        self.name = campaign_model.name
        self.description = campaign_model.description
        self.campaign_picture_url = campaign_model.campaign_picture_url
        self.alt_model_pictures_url = campaign_model.images
        self.printer = User(campaign_model.printer.user)
        self.pledge_price = float(campaign_model.pledge_price)
        self.start_date = campaign_model.start_date
        self.end_date = campaign_model.end_date
        self.min_pledgers = campaign_model.min_pledgers
        self.max_pledgers = campaign_model.max_pledgers
        self.current_pledgers = len(campaign_model.pledges)
        self.tech_datails = TechDetail(campaign_model.tech_detail)

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "campaign_picture_url": self.campaign_picture_url,
            "printer": self.printer.to_json(),
            "pledge_price": self.pledge_price,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "min_pledgers": self.min_pledgers,
            "max_pledgers": self.max_pledgers,
            "current_pledgers": self.current_pledgers,
            "tech_details": self.tech_datails.to_json()
        }
