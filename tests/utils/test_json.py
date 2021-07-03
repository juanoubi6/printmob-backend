from tests.utils.mock_entities import MOCK_CAMPAIGN_MODEL_IMAGE

GET_PLEDGES_RESPONSE_JSON = [
    {
        'buyer_id': 1,
        'campaign_id': 1,
        'created_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'deleted_at': None,
        'id': 1,
        'pledge_price': 350.0,
        'updated_at': 'Sun, 17 May 2020 00:00:00 GMT'
    }
]

UPDATE_ORDER_RESPONSE_JSON = {
    'buyer': {
        'address': {
            'address': 'Calle falsa 123',
            'apartment': 'A',
            'city': 'CABA',
            'floor': '7',
            'id': 1,
            'province': 'CABA',
            'zip_code': 'C1425'
        },
        'created_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
        'deleted_at': None,
        'email': 'email@email.com',
        'first_name': 'John',
        'id': 1,
        'last_name': 'Doe',
        'updated_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'user_name': 'johnDoe5'
    },
    'comments': 'comments',
    'id': 1,
    'mail_company': 'mail_company',
    'status': 'In progress',
    'tracking_code': 'tracking_code'
}

UPDATE_ORDER_REQUEST_JSON = {
    "status": "Dispatched",
    "mail_company": "OCA",
    "tracking_code": "1234",
    "comments": "Comment"
}

UPDATE_ORDER_STATUSES_MASSIVE_REQUEST_JSON = {
    "order_ids": [1, 2, 3],
    "status": "Dispatched"
}

PLEDGE_POST_REQUEST_JSON = {
    "buyer_id": 1,
    "campaign_id": 1,
    "pledge_price": 350.0
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
    "deleted_at": None,
    "status": "In progress"
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
    "updated_at": "Sun, 17 May 2020 00:00:00 GMT",
    "status": "In progress"
}

CAMPAIGN_MODEL_IMAGE_JSON = {
    "id": MOCK_CAMPAIGN_MODEL_IMAGE.id,
    "campaign_id": MOCK_CAMPAIGN_MODEL_IMAGE.campaign_id,
    "model_picture_url": MOCK_CAMPAIGN_MODEL_IMAGE.model_picture_url
}

CAMPAIGN_BUYERS_JSON_RESPONSE = [
    {
        'address': {
            'address': 'Calle falsa 123',
            'apartment': 'A',
            'city': 'CABA',
            'floor': '7',
            'id': 1,
            'province': 'CABA',
            'zip_code': 'C1425'
        },
        'created_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
        'deleted_at': None,
        'email': 'email@email.com',
        'first_name': 'John',
        'id': 1,
        'last_name': 'Doe',
        'updated_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'user_name': 'johnDoe5'
    }
]
