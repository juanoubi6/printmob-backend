class Campaign:
    def __init__(self, name, campaign_id):
        self.id = campaign_id
        self.name = name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
