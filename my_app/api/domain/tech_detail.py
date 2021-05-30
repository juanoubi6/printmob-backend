class TechDetail:
    def __init__(self, tech_detail_model):
        self.id = tech_detail_model.id
        self.campaign_id = tech_detail_model.campaign_id
        self.material = tech_detail_model.material
        self.weight = tech_detail_model.weight
        self.width = tech_detail_model.width
        self.length = tech_detail_model.length
        self.depth = tech_detail_model.depth

    def to_json(self):
        return {
            "dimension": {
                "weight": self.weight,
                "width": self.width,
                "length": self.length,
                "depth": self.depth
            },
            "material": self.material
        }
