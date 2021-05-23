from my_app.api.domain import User
from my_app.api.repositories.models import UserModel


class TestRepository:
    def __init__(self, db):
        self.db = db

    def get_test_data_from_db(self):
        user_model = UserModel(name='Name', full_name='FullName', nick_name="NickName")
        self.db.session.add(user_model)
        self.db.session.commit()

        user_model = self.db.session.query(UserModel).filter_by(name='Name').first()
        return User(user_model.name, user_model.full_name, user_model.nick_name)
