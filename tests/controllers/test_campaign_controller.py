import datetime
from unittest.mock import patch

from my_app.api import create_app
from my_app.api.domain import Campaign, CampaignModelImage, Printer, User, TechDetail

app = create_app()
app.config['TESTING'] = True
app.testing = True
client = app.test_client()


@patch.object(app.campaign_controller, "campaign_service")
def test_get_campaigns_returns_campaign_list(mock_campaign_service):
    mock_campaign_service.get_campaigns.return_value = [MOCK_CAMPAIGN]

    res = client.get("/campaigns")
    assert res.json[0]["name"] == MOCK_CAMPAIGN.name


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
        date_of_birth=datetime.datetime.now(),
        email="email@email.com"
    )),
    pledge_price=10.50,
    start_date=datetime.datetime.now(),
    end_date=datetime.datetime.now(),
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
