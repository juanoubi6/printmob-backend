import os

DEBUG = True

ENV = os.environ["ENVIRONMENT"]

DB_CONFIG = {
    "test": {
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    },
    "develop": {
        "SQLALCHEMY_DATABASE_URI": os.environ["DATABASE_URL"],
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }

}
