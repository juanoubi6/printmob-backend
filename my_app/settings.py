import os

ENV = os.environ["ENV"]

DB_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": os.environ["DATABASE_URL"],
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}

AWS_BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
