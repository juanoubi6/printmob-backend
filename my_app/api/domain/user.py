class User:
    def __init__(self, name, full_name, nick_name):
        self.name = name
        self.full_name = full_name
        self.nick_name = nick_name

    def to_json(self):
        return {
            "name": self.name,
            "full_name": self.full_name,
            "nick_name": self.nick_name
        }
