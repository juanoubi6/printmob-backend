class ModelImage:
    def __init__(
            self,
            id: int,
            model_picture_url: str,
            model_id: int,
            file_name: str
    ):
        self.id = id
        self.model_picture_url = model_picture_url
        self.model_id = model_id
        self.file_name = file_name

    def to_json(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "model_picture_url": self.model_picture_url,
        }


class ModelImagePrototype:
    def __init__(
            self,
            model_picture_url: str,
            model_id: int,
            file_name: str
    ):
        self.model_picture_url = model_picture_url
        self.model_id = model_id
        self.file_name = file_name
