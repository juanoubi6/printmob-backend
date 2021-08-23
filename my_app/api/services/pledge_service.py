from typing import List

from my_app.api.domain import Pledge
from my_app.api.exceptions import CancellationException
from my_app.api.exceptions.pledge_creation_exception import PledgeCreationException
from my_app.api.repositories import PledgeRepository, CampaignRepository, MercadopagoRepository, TransactionRepository

MAX_PLEDGERS_REACHED = "No se puede realizar una reserva ya que la cantidad maxima de reservas de esta campaña ya fue alcanzada"
END_DATE_REACHED = "No se puede realizar una reserva en una campaña que ya ha finalizado"
MAX_PLEDGES_PER_CAMPAIGN_REACHED = "No podes realizar mas de una reserva en esta campaña"
PLEDGE_CANCELLATION_ON_GOAL_REACHED = "No podes cancelar una reserva una vez la campaña ha sido confirmada"


class PledgeService:
    def __init__(
            self,
            pledge_repository: PledgeRepository,
            campaign_repository: CampaignRepository,
            mercadopago_repository: MercadopagoRepository
    ):
        self.pledge_repository = pledge_repository
        self.campaign_repository = campaign_repository
        self.mercadopago_repository = mercadopago_repository

    def cancel_pledge(self, pledge_id: int):
        campaign = self.pledge_repository.get_pledge_campaign(pledge_id)

        if campaign.has_reached_confirmation_goal():
            raise CancellationException(PLEDGE_CANCELLATION_ON_GOAL_REACHED)

        self.pledge_repository.delete_pledge(pledge_id)

    def get_pledges(self, filters: dict) -> List[Pledge]:
        return self.pledge_repository.get_pledges(filters)

    def create_pledge_with_payment(self, campaign_id: int, payment_id: int, buyer_id: int) -> Pledge:
        campaign = self.campaign_repository.get_campaign_detail(campaign_id)
        if campaign.has_reached_maximum_pledgers():
            raise PledgeCreationException(MAX_PLEDGERS_REACHED)
        if campaign.has_reached_end_date():
            raise PledgeCreationException(END_DATE_REACHED)
        if self.pledge_repository.has_pledge_in_campaign(buyer_id, campaign_id):
            raise PledgeCreationException(MAX_PLEDGES_PER_CAMPAIGN_REACHED)

        confirm_campaign = campaign.has_to_be_confirmed()
        finalize_campaign = campaign.has_one_pledge_left()

        return self.pledge_repository.create_pledge_with_payment(
            campaign_id, buyer_id, payment_id, confirm_campaign, finalize_campaign
        )
