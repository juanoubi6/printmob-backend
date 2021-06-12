class TechDetail:
    def __init__(
            self,
            id: int,
            campaign_id: int,
            material: str,
            weight: int,
            width: int,
            length: int,
            depth: int
    ):
        self.id = id
        self.campaign_id = campaign_id
        self.material = material
        self.weight = weight
        self.width = width
        self.length = length
        self.depth = depth

    def to_json(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "material": self.material,
            "weight": self.weight,
            "dimensions": {
                "width": self.width,
                "length": self.length,
                "depth": self.depth
            }
        }


class TechDetailPrototype:
    def __init__(
            self,
            material: str,
            weight: int,
            width: int,
            length: int,
            depth: int
    ):
        self.material = material
        self.weight = weight
        self.width = width
        self.length = length
        self.depth = depth
