from tests.utils.mock_data import MOCK_CAMPAIGN_MODEL_IMAGE

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

CAMPAIGN_POST_RESPONSE_JSON = {
    "campaign_model_images": [],
    "campaign_picture_url": None,
    "created_at": "Sun, 17 May 2020 00:00:00 GMT",
    "current_pledgers": 2,
    "deleted_at": None,
    "description": "Description",
    "end_date": "Sun, 17 May 2020 00:00:00 GMT",
    "id": 1,
    "max_pledgers": 10,
    "min_pledgers": 5,
    "name": "Campaign name",
    "pledge_price": 10.50,
    "printer": {
        "created_at": "Sun, 17 May 2020 00:00:00 GMT",
        "date_of_birth": "Sun, 17 May 2020 00:00:00 GMT",
        "deleted_at": None,
        "email": "email@email.com",
        "first_name": "John",
        "id": 1,
        "last_name": "Doe",
        "updated_at": "Sun, 17 May 2020 00:00:00 GMT",
        "user_name": "johnDoe5"
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
    "updated_at": "Sun, 17 May 2020 00:00:00 GMT"
}

CAMPAIGN_MODEL_IMAGE_JSON = {
    "id": MOCK_CAMPAIGN_MODEL_IMAGE.id,
    "campaign_id": MOCK_CAMPAIGN_MODEL_IMAGE.campaign_id,
    "model_picture_url": MOCK_CAMPAIGN_MODEL_IMAGE.model_picture_url
}
