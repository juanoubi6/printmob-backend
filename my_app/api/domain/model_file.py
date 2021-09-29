class ModelFile:
    def __init__(
            self,
            id: int,
            model_file_url: str,
            file_name: str
    ):
        self.id = id
        self.model_file_url = model_file_url
        self.file_name = file_name

    def to_json(self):
        return {
            "id": self.id,
            "model_file_url": self.model_file_url,
        }


class ModelFilePrototype:
    def __init__(
            self,
            model_file_url: str,
            file_name: str
    ):
        self.model_file_url = model_file_url
        self.file_name = file_name
