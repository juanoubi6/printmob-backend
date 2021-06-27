import datetime

from my_app.api.domain import Campaign, Printer, User, TechDetail, Pledge, CampaignModelImage, \
    CampaignModelImagePrototype, File, CampaignStatus, Buyer, Address
from my_app.api.repositories.models import CampaignModel, TechDetailsModel, PrinterModel, UserModel, PledgeModel, \
    CampaignModelImageModel, BuyerModel, AddressModel

MOCK_CAMPAIGN = Campaign(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url=None,
    campaign_model_images=[],
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
    updated_at=datetime.datetime(2020, 5, 17),
    status=CampaignStatus.IN_PROGRESS
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
MOCK_ADDRESS_MODEL = AddressModel(
    id=1,
    address="Calle falsa 123",
    zip_code="C1425",
    province="CABA",
    city="CABA",
    floor="7",
    apartment="A"
)


MOCK_BUYER_MODEL = BuyerModel(
    id=2,
    address_id=1,
    user=MOCK_USER_MODEL,
    address=MOCK_ADDRESS_MODEL
)

MOCK_PLEDGE_MODEL = PledgeModel(
    id=1,
    campaign_id=1,
    pledge_price=1.1,
    buyer_id=1,
    buyer=MOCK_BUYER_MODEL,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_CAMPAIGN_MODEL_IMAGE_MODEL = CampaignModelImageModel(
    id=1,
    model_picture_url="url",
    campaign_id=1,
    file_name="file_name"
)

MOCK_CAMPAIGN_MODEL = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=5,
    max_pledgers=10,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    status="In progress"
)

MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=1,
    max_pledgers=2,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    status="In progress"
)

MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_REACHED = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=1,
    max_pledgers=2,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL, MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    status="In progress"
)

MOCK_FILTERS = {"page": 1, "page_size": 1}

MOCK_CAMPAIGN_MODEL_IMAGE = CampaignModelImage(
    id=1,
    campaign_id=1,
    model_picture_url="url",
    file_name="filename"
)

MOCK_CAMPAIGN_MODEL_IMAGE_PROTOTYPE = CampaignModelImagePrototype(
    campaign_id=1,
    file_name="file_name",
    model_picture_url="image_url"
)

MOCK_FILE = File(
    content=bytes(b"someImageData"),
    mimetype="image/jpeg"
)

MOCK_USER = User(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_ADDRESS = Address(
    id=1,
    address="Calle falsa 123",
    zip_code="C1425",
    province="CABA",
    city="CABA",
    floor="7",
    apartment="A"
)

MOCK_BUYER = Buyer(MOCK_USER, MOCK_ADDRESS)
