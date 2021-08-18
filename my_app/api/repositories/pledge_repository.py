import datetime
from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import noload

from my_app.api.domain import PledgePrototype, Pledge, Campaign, CampaignStatus, TransactionType
from my_app.api.exceptions import NotFoundException, MercadopagoException, BusinessException
from my_app.api.repositories import CampaignRepository, MercadopagoRepository
from my_app.api.repositories.models import PledgeModel, CampaignModel, TransactionModel
from my_app.api.repositories.utils import apply_pledge_filters

PLEDGE_NOT_FOUND = "Pledge could not be found"
PLEDGE_CAMPAIGN_NOT_FOUND = "Pledge's campaign could not be found"
MAX_PLEDGERS_REACHED = "Pledge cannot be created once the maximum number of pledgers has been reached"
PLEDGE_COULD_NOT_BE_CANCELLED = "Pledge could not be cancelled"

class PledgeRepository:
    def __init__(self, db, campaign_repository: CampaignRepository, mercadopago_repository: MercadopagoRepository):
        self.db = db
        self._campaign_repository = campaign_repository
        self._mercadopago_repository = mercadopago_repository

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

    def create_pledge(self, prototype: PledgePrototype, confirm_campaign: bool, finalize_campaign: bool) -> Pledge:
        # This just creates the pledge without the payment. The pledge will be updated with payment
        # data in another endpoint.
        pledge_model = PledgeModel(campaign_id=prototype.campaign_id,
                                   pledge_price=prototype.pledge_price,
                                   buyer_id=prototype.buyer_id)
        self.db.session.add(pledge_model)

        if finalize_campaign:
            campaign_model = self._campaign_repository.get_campaign_model_by_id(prototype.campaign_id)
            campaign_model.status = CampaignStatus.TO_BE_FINALIZED.value
            campaign_model.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        elif confirm_campaign:
            campaign_model = self._campaign_repository.get_campaign_model_by_id(prototype.campaign_id)
            campaign_model.status = CampaignStatus.CONFIRMED.value

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
        pledge_model = self.get_pledge_model_by_id(pledge_id)

        return pledge_model.to_pledge_entity()

    def has_pledge_in_campaign(self, buyer_id: int, campaign_id: int) -> bool:
        return self.db.session.query(PledgeModel) \
                   .filter(PledgeModel.campaign_id == campaign_id) \
                   .filter(PledgeModel.buyer_id == buyer_id) \
                   .filter(PledgeModel.deleted_at == None) \
                   .options(noload(PledgeModel.buyer)) \
                   .first() is not None

    # TODO: delete designer transaction in the future
    def delete_pledge(self, pledge_id: int) -> Pledge:
        try:
            # Retrieve pledge
            pledge_model = self.get_pledge_model_by_id(pledge_id)

            # Delete pledge
            pledge_model.deleted_at = datetime.datetime.now()

            # Create printer refund transaction
            printer_refund_transaction_model = TransactionModel(
                mp_payment_id=pledge_model.printer_transaction.mp_payment_id,
                user_id=pledge_model.printer_transaction.user_id,
                amount=pledge_model.printer_transaction.amount * -1,
                type=TransactionType.REFUND.value,
                is_future=pledge_model.printer_transaction.is_future,
            )
            self.db.session.add(printer_refund_transaction_model)

            # Refund mercadopago payment
            self._mercadopago_repository.refund_payment(pledge_model.printer_transaction.mp_payment_id)

            self.db.session.commit()

        except MercadopagoException as mpex:
            self.db.session.rollback()
            raise BusinessException("{}: {}".format(PLEDGE_COULD_NOT_BE_CANCELLED, str(mpex)))

        return pledge_model.to_pledge_entity()

    def get_pledge_model_by_id(self, pledge_id: int) -> PledgeModel:
        pledge_model = self.db.session.query(PledgeModel) \
            .filter_by(id=pledge_id) \
            .filter(PledgeModel.deleted_at == None) \
            .first()

        if pledge_model is None:
            raise NotFoundException(PLEDGE_NOT_FOUND)

        return pledge_model

    # TODO: create designer transaction in the future
    def create_pledge_with_payment(
            self,
            campaign_id: int,
            buyer_id: int,
            payment_id: int,
            confirm_campaign: bool,
            finalize_campaign: bool
    ) -> Pledge:
        try:
            # Retrieve payment data from mercadopago
            payment = self._mercadopago_repository.get_payment_data(payment_id)

            # Retrieve campaign data
            campaign_model = self._campaign_repository.get_campaign_model_by_id(campaign_id)

            # Create pledge printer transaction
            printer_transaction_model = TransactionModel(
                mp_payment_id=payment_id,
                user_id=campaign_model.printer.id,
                amount=payment.get_transaction_net_amount(),
                type=TransactionType.PLEDGE.value,
                is_future=True
            )
            self.db.session.add(printer_transaction_model)
            self.db.session.flush()

            pledge_model = PledgeModel(campaign_id=campaign_id,
                                       pledge_price=campaign_model.pledge_price,
                                       buyer_id=buyer_id,
                                       printer_transaction_id=printer_transaction_model.id)
            self.db.session.add(pledge_model)

            # Update campaigns if necessary
            if finalize_campaign:
                campaign_model.status = CampaignStatus.TO_BE_FINALIZED.value
                campaign_model.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
            elif confirm_campaign:
                campaign_model.status = CampaignStatus.CONFIRMED.value

            self.db.session.commit()
        except Exception as exc:
            self.db.session.rollback()
            raise BusinessException("Error creating pledge: {}".format(str(exc)))

        return pledge_model.to_pledge_entity()
