from my_app.api.domain import PledgePrototype, Pledge


class PledgeService:
    def __init__(self, pledge_repository):
        self.pledge_repository = pledge_repository

    def create_pledge(self, prototype: PledgePrototype) -> Pledge:
        return self.pledge_repository.create_pledge(prototype)
