import datetime

from my_app.api.domain import OrderStatus, UserType, TransactionType
from my_app.api.repositories.models import CampaignModel, TechDetailsModel, PrinterModel, UserModel, PledgeModel, \
    CampaignModelImageModel, BuyerModel, AddressModel, OrderModel, BankInformationModel, TransactionModel, \
    DesignerModel, ModelImageModel, ModelLikeModel, ModelCategoryModel, ModelModel, ModelFileModel, ModelPurchaseModel

MOCK_BANK_INFORMATION_MODEL = BankInformationModel(
    id=1,
    cbu="2222222222",
    alias=None,
    account_number="324324",
    bank="Galicia"
)

MOCK_PRINTER_TRANSACTION_MODEL = TransactionModel(
    mp_payment_id=12345,
    user_id=2,
    amount=150,
    type=TransactionType.PLEDGE.value,
    is_future=True,
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

MOCK_USER_PRINTER_MODEL = UserModel(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.PRINTER.value,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_USER_DESIGNER_MODEL = UserModel(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.DESIGNER.value,
    profile_picture_url="url",
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_USER_BUYER_MODEL = UserModel(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.BUYER.value,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_PRINTER_MODEL = PrinterModel(
    id=1,
    user=MOCK_USER_PRINTER_MODEL,
    bank_information=MOCK_BANK_INFORMATION_MODEL
)

MOCK_DESIGNER_MODEL = DesignerModel(
    id=1,
    user=MOCK_USER_DESIGNER_MODEL,
    bank_information=MOCK_BANK_INFORMATION_MODEL
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
    user=MOCK_USER_BUYER_MODEL,
    address=MOCK_ADDRESS_MODEL
)

MOCK_PLEDGE_MODEL = PledgeModel(
    id=1,
    campaign_id=1,
    pledge_price=1.1,
    buyer_id=1,
    buyer=MOCK_BUYER_MODEL,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    printer_transaction=MOCK_PRINTER_TRANSACTION_MODEL
)

MOCK_CAMPAIGN_MODEL_IMAGE_MODEL = CampaignModelImageModel(
    id=1,
    model_picture_url="url",
    campaign_id=1,
    file_name="file_name"
)

MOCK_MODEL_IMAGE_MODEL = ModelImageModel(
    id=1,
    model_picture_url="url",
    model_id=1,
    file_name="file_name"
)

MOCK_MODEL_LIKE_MODEL = ModelLikeModel(
    id=1,
    user_id=2,
    model_id=3
)

MOCK_MODEL_CATEGORY_MODEL = ModelCategoryModel(
    id=1,
    name="Categoria 1"
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
    status="In progress",
    mp_preference_id="preference_id"
)

MOCK_CAMPAIGN_MODEL_MAX_PLEDGES_ALMOST_REACHED = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    end_date=datetime.datetime(2030, 5, 17),
    min_pledgers=1,
    max_pledgers=2,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    status="Confirmed",
    mp_preference_id="preference_id"
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
    status="To be finalized",
    mp_preference_id="preference_id"
)

MOCK_COMPLETED_CAMPAIGN_MODEL = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=1,
    max_pledgers=10,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    status="Completed",
    mp_preference_id="preference_id"
)

MOCK_CONFIRMED_CAMPAIGN_MODEL = CampaignModel(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url="campaign picture url",
    pledge_price=10.50,
    end_date=datetime.datetime(2020, 5, 17),
    min_pledgers=1,
    max_pledgers=10,
    tech_detail=MOCK_TECH_DETAIL_MODEL,
    images=[MOCK_CAMPAIGN_MODEL_IMAGE_MODEL],
    printer=MOCK_PRINTER_MODEL,
    pledges=[MOCK_PLEDGE_MODEL],
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    status="Confirmed",
    mp_preference_id="preference_id"
)

MOCK_ORDER_MODEL = OrderModel(
    id=1,
    campaign_id=MOCK_CAMPAIGN_MODEL.id,
    pledge_id=MOCK_PLEDGE_MODEL.id,
    buyer_id=MOCK_BUYER_MODEL.id,
    status=OrderStatus.IN_PROGRESS.value,
    mail_company="mail_company",
    tracking_code="tracking_code",
    comments="comments",
    buyer=MOCK_BUYER_MODEL
)

MOCK_DISPATCHED_ORDER_MODEL = OrderModel(
    id=1,
    campaign_id=MOCK_CAMPAIGN_MODEL.id,
    pledge_id=MOCK_PLEDGE_MODEL.id,
    buyer_id=MOCK_BUYER_MODEL.id,
    status=OrderStatus.DISPATCHED.value,
    mail_company="mail_company",
    tracking_code="tracking_code",
    comments="comments",
    buyer=MOCK_BUYER_MODEL
)

MOCK_MODEL_FILE_MODEL = ModelFileModel(
    id=1,
    model_file_url="url",
    file_name="file_name"
)

MOCK_MODEL_MODEL = ModelModel(
    id=1,
    designer_id=2,
    name="name",
    description="description",
    model_file_id=1,
    model_category_id=2,
    likes=1,
    width=12,
    length=12,
    depth=12,
    mp_preference_id="preference",
    allow_purchases=True,
    allow_alliances=True,
    purchase_price=25.5,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17),
    deleted_at=None,
    designer=MOCK_DESIGNER_MODEL,
    images=[MOCK_MODEL_IMAGE_MODEL],
    model_file=MOCK_MODEL_FILE_MODEL,
    model_category=MOCK_MODEL_CATEGORY_MODEL
)

MOCK_MODEL_PURCHASE_MODEL = ModelPurchaseModel(
    id=1,
    printer_id=2,
    model_id=1,
    price=20,
    transaction_id=1,
    created_at=datetime.datetime(2020, 5, 17),
    model=MOCK_MODEL_MODEL,
    printer=MOCK_PRINTER_MODEL,
)
