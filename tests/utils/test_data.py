import datetime

from my_app.api.domain import CampaignPrototype, CampaignStatus
from my_app.api.domain import TechDetailPrototype

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
    ),
    status=CampaignStatus.IN_PROGRESS
)

