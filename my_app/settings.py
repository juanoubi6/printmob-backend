import os

ENV = os.environ["ENV"]

DB_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": os.environ["DATABASE_URL"],
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}
