from my_app.api.domain import TechDetail
from my_app.api.domain.tech_detail import TechDetailPrototype
from my_app.api.repositories.models import TechDetailsModel


class TechDetailsRepository:
    def __init__(self, db):
        self.db = db

    def create_tech_detail(self, campaign_id: int, prototype: TechDetailPrototype) -> TechDetail:
        tech_detail = TechDetailsModel(campaign_id=campaign_id,
                                       material=prototype.material,
                                       weight=prototype.weight,
                                       width=prototype.width,
                                       length=prototype.length,
                                       depth=prototype.depth)
        self.db.session.add(tech_detail)
        self.db.session.commit()

        return tech_detail.to_tech_detail_entity()
