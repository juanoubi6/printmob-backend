import datetime

from sqlalchemy import null

from my_app.api.domain import Campaign, CampaignModelImage, Printer, User, TechDetail, Pledge
from my_app.api.domain.campaign import CampaignPrototype
from my_app.api.domain.tech_detail import TechDetailPrototype
from my_app.api.repositories.models import CampaignModel, TechDetailsModel, PrinterModel, UserModel, PledgeModel, \
    CampaignModelImageModel

TEST_CAMPAIGN_PROTOTYPE = CampaignPrototype(
    name="test_campaign",
    description="test_campaign_description",
    campaign_picture_url=None,
    campaign_model_image_urls=[],
    printer_id=1,
    pledge_price=250.0,
    end_date=datetime.datetime.strptime("21-05-2022 02:00:00", '%d-%m-%Y %H:%M:%S'),
    min_pledgers=2,
    max_pledgers=3,
    tech_details=TechDetailPrototype(
        material="campaign_material",
        weight=10,
        width=12,
        length=14,
        depth=15
    )
)
