import datetime

from my_app.api.domain import Campaign, Printer, User, TechDetail, Pledge, CampaignModelImage, \
    CampaignModelImagePrototype, File, CampaignStatus, Buyer, Address, Order, OrderStatus, CampaignPrototype, \
    TechDetailPrototype, UserType, GoogleUserData, BuyerPrototype, UserPrototype, AddressPrototype, PrinterPrototype, \
    BankInformation, BankInformationPrototype, Payment, TransactionPrototype, TransactionType, Balance, \
    PrinterDataDashboard, EndingCampaignResume

MOCK_BANK_INFORMATION = BankInformation(
    id=1,
    cbu="2222222222",
    alias=None,
    account_number="324324",
    bank="Galicia"
)

MOCK_BANK_INFORMATION_PROTOTYPE = BankInformationPrototype(
    cbu="2222222222",
    alias=None,
    account_number="324324",
    bank="Galicia"
)

MOCK_CAMPAIGN = Campaign(
    id=1,
    name="Campaign name",
    description="Description",
    campaign_picture_url=None,
    campaign_model_images=[],
    printer=Printer(
        user=User(
            id=1,
            first_name="John",
            last_name="Doe",
            user_name="johnDoe5",
            date_of_birth=datetime.datetime(2020, 5, 17),
            email="email@email.com",
            user_type=UserType.PRINTER.value,
            profile_picture_url="url",
            created_at=datetime.datetime(2020, 5, 17),
            updated_at=datetime.datetime(2020, 5, 17),
        ),
        bank_information=MOCK_BANK_INFORMATION
    ),
    pledge_price=10.50,
    end_date=datetime.datetime(2023, 5, 17),
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
    status=CampaignStatus.IN_PROGRESS,
    mp_preference_id="preference_id"
)

MOCK_PLEDGE = Pledge(
    id=1,
    buyer_id=1,
    pledge_price=350.0,
    campaign_id=1,
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_FILTERS = {"page": 1, "page_size": 1, "status": "In progress,Unsatisfied"}

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

MOCK_BUYER_USER = User(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.BUYER,
    profile_picture_url="url",
    created_at=datetime.datetime(2020, 5, 17),
    updated_at=datetime.datetime(2020, 5, 17)
)

MOCK_PRINTER_USER = User(
    id=1,
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.PRINTER,
    profile_picture_url="url",
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

MOCK_BUYER = Buyer(MOCK_BUYER_USER, MOCK_ADDRESS)
MOCK_PRINTER = Printer(MOCK_PRINTER_USER, MOCK_BANK_INFORMATION)

MOCK_ORDER = Order(
    id=1,
    campaign=MOCK_CAMPAIGN,
    campaign_id=MOCK_CAMPAIGN.id,
    pledge_id=MOCK_PLEDGE.id,
    buyer=MOCK_BUYER,
    status=OrderStatus.IN_PROGRESS,
    mail_company="mail_company",
    tracking_code="tracking_code",
    comments="comments"
)

MOCK_CAMPAIGN_PROTOTYPE = CampaignPrototype(
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

MOCK_GOOGLE_USER_DATA = GoogleUserData(
    first_name="First name",
    last_name="Last name",
    email="email",
    picture="picture"
)

MOCK_PRINTER_USER_PROTOTYPE = UserPrototype(
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.PRINTER,
    profile_picture_url="url",
)

MOCK_BUYER_USER_PROTOTYPE = UserPrototype(
    first_name="John",
    last_name="Doe",
    user_name="johnDoe5",
    date_of_birth=datetime.datetime(2020, 5, 17),
    email="email@email.com",
    user_type=UserType.BUYER,
    profile_picture_url="url",
)

MOCK_ADDRESS_PROTOTYPE = AddressPrototype(
    address="Calle falsa 123",
    zip_code="C1425",
    province="CABA",
    city="CABA",
    floor="7",
    apartment="A"
)

MOCK_BUYER_PROTOTYPE = BuyerPrototype(
    user_prototype=MOCK_BUYER_USER_PROTOTYPE,
    address_prototype=MOCK_ADDRESS_PROTOTYPE
)

MOCK_PRINTER_PROTOTYPE = PrinterPrototype(
    user_prototype=MOCK_PRINTER_USER_PROTOTYPE,
    bank_information_prototype=MOCK_BANK_INFORMATION_PROTOTYPE
)

MOCK_PAYMENT = Payment(
    payment_id=123456,
    payment_data={
        "transaction_details": {
            "net_received_amount": 100
        }
    }
)

MOCK_TRANSACTION_PROTOTYPE = TransactionPrototype(
    mp_payment_id=12345,
    user_id=1,
    amount=100,
    type=TransactionType.PLEDGE,
    is_future=True
)

MOCK_BALANCE = Balance(
    current_balance=100.5,
    future_balance=25.6
)

MOCK_ENDING_CAMPAIGN_RESUME = EndingCampaignResume(
    id=1,
    name="Campaña 1",
    percentage=50,
    remaining_days=4
)

MOCK_PRINTER_DATA_DASHBOARD = PrinterDataDashboard(
    campaigns_in_progress=1,
    completed_campaigns=2,
    pledges_in_progress=3,
    balance=MOCK_BALANCE,
    pending_orders=5,
    ending_campaigns=[MOCK_ENDING_CAMPAIGN_RESUME]
)
