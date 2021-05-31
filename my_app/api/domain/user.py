class User:
    def __init__(self, user_model):
        self.id = user_model.id
        self.first_name = user_model.first_name
        self.last_name = user_model.last_name
        self.user_name = user_model.user_name
        self.date_of_birth = user_model.date_of_birth
        self.email = user_model.email

    def to_json(self):
        return {
            "user_name": self.user_name
        }
