import datetime
from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import noload

from my_app.api.domain import PledgePrototype, Pledge, Campaign, CampaignStatus
from my_app.api.exceptions import NotFoundException
from my_app.api.repositories import CampaignRepository
from my_app.api.repositories.models import PledgeModel, CampaignModel
from my_app.api.repositories.utils import apply_pledge_filters

PLEDGE_NOT_FOUND = "Pledge could not be found"
PLEDGE_CAMPAIGN_NOT_FOUND = "Pledge's campaign could not be found"
MAX_PLEDGERS_REACHED = "Pledge cannot be created once the maximum number of pledgers has been reached"


class PledgeRepository:
    def __init__(self, db, campaign_repository: CampaignRepository):
        self.db = db
        self._campaign_repository = campaign_repository

    def get_pledges(self, filters: dict) -> List[Pledge]:
        """
        Returns list of pledges that match the provided filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        """
        query = self.db.session.query(PledgeModel).filter(PledgeModel.deleted_at == None)
        query = apply_pledge_filters(query, filters)
        query = query.options(noload(PledgeModel.buyer)).order_by(asc(PledgeModel.id))

        pledge_models = query.all()

        return [pledge_model.to_pledge_entity() for pledge_model in pledge_models]

    def create_pledge(self, prototype: PledgePrototype, finalize_campaign: bool = False) -> Pledge:
        # TODO for mercadopago: we will need to add MercadopagoRepository here
        # 1- Call MercadopagoRepository and create the payment
        # 2- With the payment object, search the net transaction amount (without commissions) and calculate both the
        #    printer and designer transactions (you may not need to create a designer transaction depending on
        #    the campaign type)
        # 3- Create printer transaction
        # 4- Create designer transaction (if necessary)
        # 5- Create pledge with the previous transaction ids
        # If any of the database operation fails, try to issue a refund of the payment
        pledge_model = PledgeModel(campaign_id=prototype.campaign_id,
                                   pledge_price=prototype.pledge_price,
                                   buyer_id=prototype.buyer_id)
        self.db.session.add(pledge_model)

        if finalize_campaign:
            campaign_model = self._campaign_repository.get_campaign_model_by_id(prototype.campaign_id)
            campaign_model.status = CampaignStatus.TO_BE_FINALIZED.value

        self.db.session.commit()

        return pledge_model.to_pledge_entity()

    def get_pledge_campaign(self, pledge_id: int) -> Campaign:
        pledge = self.get_pledge(pledge_id)

        campaign_model = self.db.session.query(CampaignModel) \
            .filter_by(id=pledge.campaign_id) \
            .filter(CampaignModel.deleted_at == None) \
            .first()

        if campaign_model is None:
            raise NotFoundException(PLEDGE_CAMPAIGN_NOT_FOUND)

        return campaign_model.to_campaign_entity()

    def get_pledge(self, pledge_id: int) -> Pledge:
        pledge_model = self._get_pledge_model_by_id(pledge_id)

        return pledge_model.to_pledge_entity()

    def has_pledge_in_campaign(self, buyer_id: int, campaign_id: int) -> bool:
        return self.db.session.query(PledgeModel) \
                   .filter(PledgeModel.campaign_id == campaign_id) \
                   .filter(PledgeModel.buyer_id == buyer_id) \
                   .filter(PledgeModel.deleted_at == None) \
                   .options(noload(PledgeModel.buyer)) \
                   .first() is not None

    def delete_pledge(self, pledge_id: int) -> Pledge:
        # TODO for mercadopago: we will need to add MercadopagoRepository here
        # 1- Retrieve pledge
        # 2- Retrieve pledge's transactions (of printer and designer if applies)
        # 3- Delete pledge
        # 4- Create REFUND transactions (for printer and designer if applies)
        # 6- Call MercadopagoRepository and cancel payments
        # 7- If mercadopago fails, rollback db transaction. Else, commit db transaction
        pledge_model = self._get_pledge_model_by_id(pledge_id)
        pledge_model.deleted_at = datetime.datetime.now()

        self.db.session.commit()

        return pledge_model.to_pledge_entity()

    def _get_pledge_model_by_id(self, pledge_id: int) -> PledgeModel:
        pledge_model = self.db.session.query(PledgeModel) \
            .filter_by(id=pledge_id) \
            .filter(PledgeModel.deleted_at == None) \
            .first()

        if pledge_model is None:
            raise NotFoundException(PLEDGE_NOT_FOUND)

        return pledge_model
