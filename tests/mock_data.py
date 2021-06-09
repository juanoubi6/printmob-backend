import datetime

from sqlalchemy import null

from my_app.api.domain import Campaign, CampaignModelImage, Printer, User, TechDetail, Pledge
from my_app.api.repositories.models import CampaignModel, TechDetailsModel, PrinterModel, UserModel, PledgeModel, \
    CampaignModelImageModel

MOCK_CAMPAIGN = Campaign(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    campaign_model_images=[CampaignModelImage(1, "model image url", 1)],
    printer=Printer(User(
        id=1,
        first_name="John",
        last_name="Doe",
        user_name="johnDoe5",
        date_of_birth=datetime.datetime(2020, 5, 17),
        email="email@email.com",
        created_at=datetime.datetime(2020, 5, 17),
        updated_at=datetime.datetime(2020, 5, 17)
    )),
    pledge_price=10.50,
    start_date=datetime.datetime(2020, 5, 17),
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=5,
    max_pledgers=10,
    current_pledgers=2,
    tech_details=TechDetail(
        id=1,
        campaign_id=1,
        material="material",
        weight=100,
        width=100,
        length=100,
        depth=100,
    ),
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_PLEDGE = Pledge(
    id=1,
    buyer_id=1,
    pledge_price=350.0,
    campaign_id=1,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_TECH_DETAIL_MODEL = TechDetailsModel(
    id=1,
    campaign_id=1,
    material="material",
    weight=100,
    width=100,
    length=100,
    depth=100
)

MOCK_USER_MODEL = UserModel(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_PRINTER_MODEL = PrinterModel(
    id=1,
    user=MOCK_USER_MODEL
)

MOCK_PLEDGE_MODEL = PledgeModel(
    id=1,
    campaign_id=1,
    pledge_price=1.1,
    buyer_id=1,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_CAMPAIGN_MODEL_IMAGE_MODEL = CampaignModelImageModel(
    id=1,
    model_picture_url="url",
    campaign_id=1
)

MOCK_CAMPAIGN_MODEL = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    start_date=datetime.datetime(2020, 5, 17),
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=5,
    max_pledgers=10,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_FILTERS = {"page": 1, "page_size": 1}
