import io

from tests.test_utils.mock_entities import MOCK_CAMPAIGN_MODEL_IMAGE, MOCK_MODEL_IMAGE

GET_BUYER_PROFILE_RESPONSE_JSON = {
    'address': {
        'address': 'Calle falsa 123',
        'apartment': 'A',
        'city': 'CABA',
        'floor': '7',
        'id': 1,
        'province': 'CABA',
        'zip_code': 'C1425'
    },
    'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
    'email': 'email@email.com',
    'first_name': 'John',
    'id': 1,
    'last_name': 'Doe',
    'user_name': 'johnDoe5',
    'profile_picture_url': "url",
    'user_type': 'Buyer'
}

GET_PRINTER_PROFILE_RESPONSE_JSON = {
    'bank_information': {
        'account_number': '324324',
        'alias': None,
        'bank': 'Galicia',
        'cbu': '2222222222',
        'id': 1
    },
    'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
    'email': 'email@email.com',
    'first_name': 'John',
    'id': 1,
    'last_name': 'Doe',
    'user_name': 'johnDoe5',
    'profile_picture_url': "url",
    'user_type': 'Printer'
}

GET_DESIGNER_PROFILE_RESPONSE_JSON = {
    'bank_information': {
        'account_number': '324324',
        'alias': None,
        'bank': 'Galicia',
        'cbu': '2222222222',
        'id': 1
    },
    'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
    'email': 'email@email.com',
    'first_name': 'John',
    'id': 1,
    'last_name': 'Doe',
    'user_name': 'johnDoe5',
    'profile_picture_url': "url",
    'user_type': 'Designer'
}

GET_BALANCE_RESPONSE_JSON = {
    'current_balance': 100.5,
    'future_balance': 25.6
}

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
        'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
        'email': 'email@email.com',
        'first_name': 'John',
        "user_type": "Buyer",
        'last_name': 'Doe',
        'id': 1,
        'profile_picture_url': "url",
        'user_name': 'johnDoe5'
    },
    'comments': 'comments',
    'id': 1,
    'mail_company': 'mail_company',
    'status': 'In progress',
    'tracking_code': 'tracking_code',
    'campaign': {
        'alliance_percentages': None,
        'campaign_model_images': [],
        'campaign_picture_url': None,
        'created_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'current_pledgers': 2,
        'deleted_at': None,
        'description': 'Description',
        'end_date': 'Wed, 17 May 2023 00:00:00 GMT',
        'id': 1,
        'max_pledgers': 10,
        'min_pledgers': 5,
        'mp_preference_id': 'preference_id',
        'name': 'Campaign name',
        'pledge_price': 10.5,
        'printer': {'bank_information': {'account_number': '324324',
                                         'alias': None,
                                         'bank': 'Galicia',
                                         'cbu': '2222222222',
                                         'id': 1},
                    'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
                    'email': 'email@email.com',
                    'first_name': 'John',
                    'id': 1,
                    'last_name': 'Doe',
                    'profile_picture_url': 'url',
                    'user_name': 'johnDoe5',
                    'user_type': 'Printer'},
        'status': 'In progress',
        'tech_details': {'campaign_id': 1,
                         'dimensions': {'depth': 100,
                                        'length': 100,
                                        'width': 100},
                         'id': 1,
                         'material': 'material',
                         'weight': 100},
        'updated_at': 'Sun, 17 May 2020 00:00:00 GMT',
        "model_id": None,
        'designer': None
    },
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
    "alliance_percentages": None,
    "campaign_model_images": [],
    "campaign_picture_url": None,
    "current_pledgers": 2,
    "description": "Description",
    "end_date": "Wed, 17 May 2023 00:00:00 GMT",
    "id": 1,
    "max_pledgers": 10,
    "min_pledgers": 5,
    "name": "Campaign name",
    "pledge_price": 10.5,
    "printer": {
        "date_of_birth": "Sun, 17 May 2020 00:00:00 GMT",
        "email": "email@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_name": "johnDoe5",
        "user_type": "Printer",
        'profile_picture_url': "url",
        'id': 1,
        'bank_information': {
            'account_number': '324324',
            'alias': None,
            'bank': 'Galicia',
            'cbu': '2222222222',
            'id': 1
        }
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
    "status": "In progress",
    'mp_preference_id': 'preference_id',
    "model_id": None,
    'designer': None
}

CAMPAIGN_POST_REQUEST_JSON = {
    "name": "Un vaso de cala",
    "description": "Un modelo 3D para vender ::??",
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

CAMPAIGN_FROM_MODEL_POST_REQUEST_JSON = {
    "name": "Un vaso de cala",
    "description": "Un modelo 3D para vender ::??",
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
    },
    "model_id": 99
}

CAMPAIGN_POST_RESPONSE_JSON = {
    "alliance_percentages": None,
    "campaign_model_images": [],
    "campaign_picture_url": None,
    "created_at": "Sun, 17 May 2020 00:00:00 GMT",
    "current_pledgers": 2,
    "deleted_at": None,
    "description": "Description",
    "end_date": "Wed, 17 May 2023 00:00:00 GMT",
    "id": 1,
    "max_pledgers": 10,
    "min_pledgers": 5,
    "name": "Campaign name",
    "pledge_price": 10.50,
    "printer": {
        "date_of_birth": "Sun, 17 May 2020 00:00:00 GMT",
        "email": "email@email.com",
        "first_name": "John",
        "user_type": "Printer",
        "last_name": "Doe",
        'id': 1,
        "user_name": "johnDoe5",
        'profile_picture_url': "url",
        'bank_information': {
            'account_number': '324324',
            'alias': None,
            'bank': 'Galicia',
            'cbu': '2222222222',
            'id': 1
        }
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
    "status": "In progress",
    'mp_preference_id': 'preference_id',
    "model_id": None,
    'designer': None
}

CAMPAIGN_MODEL_IMAGE_JSON = {
    "id": MOCK_CAMPAIGN_MODEL_IMAGE.id,
    "campaign_id": MOCK_CAMPAIGN_MODEL_IMAGE.campaign_id,
    "model_picture_url": MOCK_CAMPAIGN_MODEL_IMAGE.model_picture_url
}

MODEL_IMAGE_JSON = {
    "id": MOCK_MODEL_IMAGE.id,
    "model_id": MOCK_MODEL_IMAGE.model_id,
    "model_picture_url": MOCK_MODEL_IMAGE.model_picture_url
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
        "user_type": "Buyer",
        'updated_at': 'Sun, 17 May 2020 00:00:00 GMT',
        'profile_picture_url': "url",
        'user_name': 'johnDoe5'
    }
]

LOGIN_RESPONSE_JSON = {
    'token': 'JWT',
    'type': 'Buyer',
    'user_data': {
        'address': {
            'address': 'Calle falsa 123',
            'apartment': 'A',
            'city': 'CABA',
            'floor': '7',
            'id': 1,
            'province': 'CABA',
            'zip_code': 'C1425'
        },
        'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
        'email': 'email@email.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'user_name': 'johnDoe5',
        'user_type': 'Buyer',
        'profile_picture_url': "url",
        'id': 1
    }
}

CREATE_PRINTER_JSON_REQUEST = {
    "first_name": "Juan",
    "last_name": "Perez",
    "user_name": "juanperez1211",
    "date_of_birth": "21-05-2023",
    "email": "juanperez11@gmail.com",
    "bank_information": {
        "cbu": "222222222333333333344",
        "alias": None,
        "bank": "Galicia",
        "account_number": "26163-44"
    }
}

CREATE_DESIGNER_JSON_REQUEST = {
    "first_name": "Juan",
    "last_name": "Perez",
    "user_name": "juanperez1211",
    "date_of_birth": "21-05-2023",
    "email": "juanperez11@gmail.com",
    "profile_picture_url": "url",
    "bank_information": {
        "cbu": "222222222333333333344",
        "alias": None,
        "bank": "Galicia",
        "account_number": "26163-44"
    }
}

CREATE_BUYER_JSON_REQUEST = {
    "first_name": "Juan",
    "last_name": "Perez",
    "user_name": "juanperez122",
    "date_of_birth": "21-05-2023",
    "email": "juanperez1@gmail.com",
    "address": {
        "address": "Calle falsa 123",
        "zip_code": "1425",
        "province": "CABA",
        "city": "CABA",
        "floor": "7",
        "apartment": None
    }
}

PRINTER_DATA_DASHBOARD_RESPONSE_JSON = {
    'balance': {'current_balance': 100.5, 'future_balance': 25.6},
    'campaigns_in_progress': 1,
    'completed_campaigns': 2,
    'pending_orders': 5,
    'pledges_in_progress': 3,
    'ending_campaigns': [
        {
            'id': 1,
            'name': 'Campaña 1',
            'percentage': 50,
            'end_date': 'Sun, 17 May 2020 00:00:00 GMT'
        }
    ],
}

DESIGNER_DATA_DASHBOARD_RESPONSE_JSON = {
    'alliances_income': 200.0,
    'balance': {'current_balance': 100.5, 'future_balance': 25.6},
    'model_purchase_income': 300.0,
    'total_likes': 50,
    'uploaded_models': 40
}

BUYER_DATA_DASHBOARD_RESPONSE_JSON = {
    'completed_orders': 3,
    'ending_campaigns': [
        {
            'end_date': 'Sun, 17 May 2020 00:00:00 GMT',
            'id': 1,
            'name': 'Campaña 1',
            'percentage': 50
        }
    ],
    'in_progress_orders': 2,
    'take_part_campaigns': 200
}

CREATE_MODEL_REQUEST = {
    "name": "Model name",
    "description": "Model description",
    "model_category_id": "1",
    "width": "2",
    "length": "3",
    "depth": "4",
    "allow_purchases": "true",
    "allow_alliances": "false",
    "purchase_price": "25.5",
    "model_file": (io.BytesIO(b"someStlFileData"), 'testStlFile.stl'),
    "image[]": (io.BytesIO(b"someImageData"), 'image1.jpg'),
    "image[]": (io.BytesIO(b"someImageData"), 'image2.jpg')
}

CREATE_MODEL_RESPONSE_JSON = {
    "allow_alliances": False,
    "allow_purchases": True,
    "depth": 4,
    "description": "Model description",
    "designer": {
        'bank_information': {
            'account_number': '324324',
            'alias': None,
            'bank': 'Galicia',
            'cbu': '2222222222',
            'id': 1
        },
        'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
        'email': 'email@email.com',
        'first_name': 'John',
        'id': 1,
        'last_name': 'Doe',
        'user_name': 'johnDoe5',
        'profile_picture_url': "url",
        'user_type': 'Designer'
    },
    "id": 1,
    "length": 3,
    "likes": 4,
    "model_file": {
        "id": 1,
        "model_file_url": "url"
    },
    "model_images": [{'id': 1, 'model_id': 1, 'model_picture_url': 'url'}],
    "mp_preference_id": "preference_id",
    "name": "Model name",
    "purchase_price": 25.5,
    'desired_percentage': 20,
    "width": 2,
    'liked_by_user': None,
    'model_category': {'id': 1, 'name': 'Categoria 1'}
}

GET_USER_LIKED_MODEL_DETAIL_JSON_RESPONSE = {
    'allow_alliances': False,
    'allow_purchases': True,
    'depth': 4,
    'description': 'Model description',
    'designer': {'bank_information': {'account_number': '324324',
                                      'alias': None,
                                      'bank': 'Galicia',
                                      'cbu': '2222222222',
                                      'id': 1},
                 'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
                 'email': 'email@email.com',
                 'first_name': 'John',
                 'id': 1,
                 'last_name': 'Doe',
                 'profile_picture_url': 'url',
                 'user_name': 'johnDoe5',
                 'user_type': 'Designer'},
    'id': 1,
    'length': 3,
    'likes': 4,
    'model_category': {'id': 1, 'name': 'Categoria 1'},
    'model_file': {'id': 1, 'model_file_url': 'url'},
    'model_images': [{'id': 1, 'model_id': 1, 'model_picture_url': 'url'}],
    'mp_preference_id': 'preference_id',
    'name': 'Model name',
    'purchase_price': 25.5,
    'desired_percentage': 20,
    'width': 2,
    'liked_by_user': True
}

GET_NEUTRAL_MODEL_DETAIL_JSON_RESPONSE = {
    'allow_alliances': False,
    'allow_purchases': True,
    'depth': 4,
    'description': 'Model description',
    'designer': {'bank_information': {'account_number': '324324',
                                      'alias': None,
                                      'bank': 'Galicia',
                                      'cbu': '2222222222',
                                      'id': 1},
                 'date_of_birth': 'Sun, 17 May 2020 00:00:00 GMT',
                 'email': 'email@email.com',
                 'first_name': 'John',
                 'id': 1,
                 'last_name': 'Doe',
                 'profile_picture_url': 'url',
                 'user_name': 'johnDoe5',
                 'user_type': 'Designer'},
    'id': 1,
    'length': 3,
    'likes': 4,
    'model_category': {'id': 1, 'name': 'Categoria 1'},
    'model_file': {'id': 1, 'model_file_url': 'url'},
    'model_images': [{'id': 1, 'model_id': 1, 'model_picture_url': 'url'}],
    'mp_preference_id': 'preference_id',
    'name': 'Model name',
    'purchase_price': 25.5,
    'desired_percentage': 20,
    'width': 2,
    'liked_by_user': None
}
