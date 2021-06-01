import datetime
import json
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


@patch.object(app.campaign_controller, "campaign_service")
def test_get_campaign_detail_returns_campaign_json(mock_campaign_service):
    mock_campaign_service.get_campaign_detail.return_value = MOCK_CAMPAIGN

    res = client.get("/campaigns/1")
    assert res.status_code == 200
    assert json.loads(res.data.decode("utf-8")) == {
        "campaign_model_images": [
            {
                "campaign_id": 1,
                "id": 1,
                "model_picture_url": "model image url"
            }
        ],
        "campaign_picture_url": "campaign picture url",
        "current_pledgers": 2,
        "description": "Description",
        "end_date": "Sun, 17 May 2020 00:00:00 GMT",
        "id": 1,
        "max_pledgers": 10,
        "min_pledgers": 5,
        "name": "Campaign name",
        "pledge_price": 10.5,
        "printer": {
            "date_of_birth": "Sun, 17 May 2020 00:00:00 GMT",
            "email": "email@email.com",
            "first_name": "John",
            "id": 1,
            "last_name": "Doe",
            "user_name": "johnDoe5"
        },
        "start_date": "Sun, 17 May 2020 00:00:00 GMT",
        "tech_details": {
            "campaign_id": 1,
            "dimensions": {
                "depth": 100,
                "length": 100,
                "width": 100
            },
            "id": 1,
            "material": "material",
            "weight": 100
        }
    }


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
