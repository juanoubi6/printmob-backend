from typing import List

from my_app.api.domain import PledgePrototype, Pledge
from my_app.api.exceptions import CancellationException
from my_app.api.exceptions.pledge_creation_exception import PledgeCreationException
from my_app.api.repositories import PledgeRepository, CampaignRepository

MAX_PLEDGERS_REACHED = "Pledge cannot be created once the maximum number of pledgers has been reached"
END_DATE_REACHED = "Pledge cannot be created once the campaign has finished"
MAX_PLEDGES_PER_CAMPAIGN_REACHED = "You can't pledge more than once in this campaign"
PLEDGE_CANCELLATION_ON_GOAL_REACHED = "Pledge cannot be cancelled once the goal has been reached"


class PledgeService:
    def __init__(self, pledge_repository: PledgeRepository, campaign_repository: CampaignRepository):
        self.pledge_repository = pledge_repository
        self.campaign_repository = campaign_repository

    def create_pledge(self, prototype: PledgePrototype) -> Pledge:
        campaign = self.campaign_repository.get_campaign_detail(prototype.campaign_id)
        if campaign.has_reached_maximum_pledgers():
            raise PledgeCreationException(MAX_PLEDGERS_REACHED)
        if campaign.has_reached_end_date():
            raise PledgeCreationException(END_DATE_REACHED)
        if self.pledge_repository.has_pledge_in_campaign(prototype.buyer_id, prototype.campaign_id):
            raise PledgeCreationException(MAX_PLEDGES_PER_CAMPAIGN_REACHED)

        finalize_campaign = campaign.has_one_pledge_left()

        return self.pledge_repository.create_pledge(prototype, finalize_campaign)

    def cancel_pledge(self, pledge_id: int):
        campaign = self.pledge_repository.get_pledge_campaign(pledge_id)

        if campaign.has_reached_confirmation_goal():
            raise CancellationException(PLEDGE_CANCELLATION_ON_GOAL_REACHED)

        self.pledge_repository.delete_pledge(pledge_id)

    def get_pledges(self, filters: dict) -> List[Pledge]:
        return self.pledge_repository.get_pledges(filters)
