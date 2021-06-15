from my_app.api.domain import PledgePrototype, Pledge
from my_app.api.exceptions import CancellationException


class PledgeService:
    def __init__(self, pledge_repository):
        self.pledge_repository = pledge_repository

    def create_pledge(self, prototype: PledgePrototype) -> Pledge:
        return self.pledge_repository.create_pledge(prototype)

    def cancel_pledge(self, pledge_id: int):
        campaign = self.pledge_repository.get_pledge_campaign(pledge_id)

        if campaign.has_reached_goal():
            raise CancellationException("Pledge cannot be cancelled once the goal has been reached")

        self.pledge_repository.delete_pledge(pledge_id)
