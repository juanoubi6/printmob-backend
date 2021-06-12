import datetime

from sqlalchemy import null

from my_app.api.domain import Campaign, CampaignModelImage, Printer, User, TechDetail, Pledge
from my_app.api.domain.campaign import CampaignPrototype
from my_app.api.domain.tech_detail import TechDetailPrototype
from my_app.api.repositories.models import CampaignModel, TechDetailsModel, PrinterModel, UserModel, PledgeModel, \
    CampaignModelImageModel

PLEDGE_POST_REQUEST_JSON = {
    "buyer_id": 1,
    "pledge_price": 350.0,
    "campaign_id": 1
}

CAMPAIGN_GET_RESPONSE_JSON = {
    "campaign_model_images": [],
    "campaign_picture_url": None,
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
        "user_name": "johnDoe5",
        "created_at": "Sun, 17 May 2020 00:00:00 GMT",
        "updated_at": "Sun, 17 May 2020 00:00:00 GMT",
        "deleted_at": None
    },
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
    },
    "created_at": "Sun, 17 May 2020 00:00:00 GMT",
    "updated_at": "Sun, 17 May 2020 00:00:00 GMT",
    "deleted_at": None
}

CAMPAIGN_POST_REQUEST_JSON = {
    "name": "Un vaso de cala",
    "description": "Un modelo 3D para vender",
    "campaign_picture_url": "https://free3d.com/imgd/l80/1089781.jpg",
    "campaign_model_image_urls": [
        "https://free3d.com/imgd/l80/1089781.jpg",
        "https://free3d.com/imgd/l80/1089782.jpg",
        "https://free3d.com/imgd/l80/1089783.jpg"
    ],
    "printer_id": 1,
    "pledge_price": 20.0,
    "end_date": "21-05-2023 01:00:00",
    "min_pledgers": 6,
    "max_pledgers": 7,
    "tech_details": {
        "material": "PLA",
        "depth": 7,
        "length": 80,
        "width": 81,
        "weight": 82
    }
}