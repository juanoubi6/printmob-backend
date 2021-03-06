import os

ENV = os.environ["ENV"]

DB_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": os.environ["DATABASE_URL"],
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}

AWS_BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]

SENDER_EMAIL = os.environ["SENDER_EMAIL"]

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_AUTH_FALLBACK_URL = os.environ["GOOGLE_AUTH_FALLBACK_URL"]

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

MERCADOPAGO_ACCESS_TOKEN = os.environ["MERCADOPAGO_ACCESS_TOKEN"]
PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT = os.environ["PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT"]
PREFERENCE_BACK_URL_FOR_SUCCESS_MODEL_PURCHASE_PAYMENT = os.environ["PREFERENCE_BACK_URL_FOR_SUCCESS_MODEL_PURCHASE_PAYMENT"]
PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS = os.environ["PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS"]
PREFERENCE_BACK_URL_FOR_MODEL_PURCHASE_ERRORS = os.environ["PREFERENCE_BACK_URL_FOR_MODEL_PURCHASE_ERRORS"]
