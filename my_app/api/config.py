db_config = {
    "test": {
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    },
    "develop": {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:1234@localhost:5432/printmob",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }

}
