class Campaign:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
