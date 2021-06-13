class File:
    def __init__(
            self,
            content: bytes,
            mimetype: str,
    ):
        self.content = content
        self.mimetype = mimetype
