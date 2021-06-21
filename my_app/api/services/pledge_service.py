from my_app.api.domain import PledgePrototype, Pledge
from my_app.api.exceptions import CancellationException
from my_app.api.exceptions.pledge_creation_exception import PledgeCreationException


class PledgeService:
    def __init__(self, pledge_repository, campaign_repository):
        self.pledge_repository = pledge_repository
        self.campaign_repository = campaign_repository

    def create_pledge(self, prototype: PledgePrototype) -> Pledge:
        campaign = self.campaign_repository.get_campaign_detail(prototype.campaign_id)
        if campaign.has_reached_maximum_pledgers():
            raise PledgeCreationException("Pledge cannot be created once the maximum number of pledgers has been "
                                          "reached")
        #TODO If max pledgers is reached the campaign must finalize
        return self.pledge_repository.create_pledge(prototype)

    def cancel_pledge(self, pledge_id: int):
        campaign = self.pledge_repository.get_pledge_campaign(pledge_id)

        if campaign.has_reached_confirmation_goal():
            raise CancellationException("Pledge cannot be cancelled once the goal has been reached")

        self.pledge_repository.delete_pledge(pledge_id)
