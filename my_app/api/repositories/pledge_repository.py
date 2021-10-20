import datetime
from typing import List

from sqlalchemy import asc
from sqlalchemy.orm import noload

from my_app.api.domain import Pledge, Campaign, CampaignStatus, TransactionType
from my_app.api.exceptions import NotFoundException, MercadopagoException, BusinessException
from my_app.api.repositories import CampaignRepository, MercadopagoRepository
from my_app.api.repositories.models import PledgeModel, CampaignModel, TransactionModel, ModelModel
from my_app.api.repositories.utils import apply_pledge_filters

PLEDGE_NOT_FOUND = "La reserva no pudo ser encontrada"
PLEDGE_CAMPAIGN_NOT_FOUND = "La campaña de la reserva no pudo ser ncontrada"
MAX_PLEDGERS_REACHED = "No se puede crear una reserva una vez que la campaña ha alcanzado el máximo de reservas posibles"
PLEDGE_COULD_NOT_BE_CANCELLED = "La reserva no pudo ser cancelada"


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

            # Create designer refund transaction if necessary
            if pledge_model.designer_transaction is not None:
                designer_refund_transaction_model = TransactionModel(
                    mp_payment_id=pledge_model.designer_transaction.mp_payment_id,
                    user_id=pledge_model.designer_transaction.user_id,
                    amount=pledge_model.designer_transaction.amount * -1,
                    type=TransactionType.REFUND.value,
                    is_future=pledge_model.designer_transaction.is_future,
                )
                self.db.session.add(designer_refund_transaction_model)

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

            # Check if campaign has an associated model. If so, create designer transaction
            printer_transaction_amount = payment.get_transaction_net_amount()
            designer_transaction_id = None

            if campaign_model.model_id is not None:
                model_model = self.db.session.query(ModelModel) \
                    .filter(ModelModel.id == campaign_model.model_id) \
                    .options(
                        noload(ModelModel.model_file),
                        noload(ModelModel.images),
                        noload(ModelModel.model_category),
                    ).first()

                designer_percentage = (model_model.desired_percentage / 100)
                printer_percentage = 1 - designer_percentage

                designer_transaction_amount = payment.get_transaction_net_amount() * float(designer_percentage)
                printer_transaction_amount = payment.get_transaction_net_amount() * float(printer_percentage)

                # Create pledge designer transaction
                designer_transaction_model = TransactionModel(
                    mp_payment_id=payment_id,
                    user_id=model_model.designer.id,
                    amount=designer_transaction_amount,
                    type=TransactionType.PLEDGE.value,
                    is_future=True
                )
                self.db.session.add(designer_transaction_model)
                self.db.session.flush()
                designer_transaction_id = designer_transaction_model.id

            # Create pledge printer transaction
            printer_transaction_model = TransactionModel(
                mp_payment_id=payment_id,
                user_id=campaign_model.printer.id,
                amount=printer_transaction_amount,
                type=TransactionType.PLEDGE.value,
                is_future=True
            )
            self.db.session.add(printer_transaction_model)
            self.db.session.flush()

            pledge_model = PledgeModel(campaign_id=campaign_id,
                                       pledge_price=campaign_model.pledge_price,
                                       buyer_id=buyer_id,
                                       printer_transaction_id=printer_transaction_model.id,
                                       designer_transaction_id=designer_transaction_id)
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
            raise BusinessException("Ocurrió un error al crear la reserva: {}".format(str(exc)))

        return pledge_model.to_pledge_entity()
