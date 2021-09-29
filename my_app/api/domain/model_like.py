class ModelLike:
    def __init__(
            self,
            id: int,
            model_id: int,
            user_id: int
    ):
        self.id = id
        self.model_id = model_id
        self.user_id = user_id

    def to_json(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "user_id": self.user_id,
        }
