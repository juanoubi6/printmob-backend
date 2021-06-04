import datetime

from my_app.api.domain import Campaign, CampaignModelImage, Printer, User, TechDetail, Pledge

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
        email="email@email.com"
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
    )
)

MOCK_PLEDGE = Pledge(
    id=1,
    buyer_id=1,
    pledge_price=350.0,
    campaign_id=1,
    pledge_date=datetime.datetime(2020, 5, 17),
)
