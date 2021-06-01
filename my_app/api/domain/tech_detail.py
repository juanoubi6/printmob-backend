from my_app.api.repositories.models import TechDetailsModel


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

    @staticmethod
    def from_model(tech_detail_model: TechDetailsModel):
        return TechDetail(
            id=tech_detail_model.id,
            campaign_id=tech_detail_model.campaign_id,
            material=tech_detail_model.material,
            weight=tech_detail_model.weight,
            width=tech_detail_model.width,
            length=tech_detail_model.length,
            depth=tech_detail_model.depth,
        )

    def to_json(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "material": self.material,
            "weight": self.weight,
            "dimension": {
                "width": self.width,
                "length": self.length,
                "depth": self.depth
            }
        }
