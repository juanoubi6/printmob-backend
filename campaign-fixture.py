import copy
import os
import datetime

import mercadopago
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_app.api.domain import CampaignStatus, OrderStatus, TransactionType
from my_app.api.repositories import MercadopagoRepository
from my_app.api.repositories.models import CampaignModel, PledgeModel, OrderModel, TechDetailsModel, TransactionModel

engine = create_engine(os.environ["DATABASE_URL"])
db_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
mercadopago_repository = MercadopagoRepository(
    mercadopago.SDK(os.environ["MERCADOPAGO_ACCESS_TOKEN"]),
    os.environ["PREFERENCE_BACK_URL_FOR_PAYMENT_ERRORS"],
    os.environ["PREFERENCE_BACK_URL_FOR_SUCCESS_PLEDGE_PAYMENT"]
)

# Change with your own printer and buyer account IDs
PRINTER_ID = 1
BUYER_ID = 2

# Buyers IDs (don't use your own)
ADDITIONAL_BUYER_ID_1 = 5
ADDITIONAL_BUYER_ID_2 = 7
ADDITIONAL_BUYER_ID_3 = 9

common_tech_detail_model = TechDetailsModel(
    material="Material",
    weight=10,
    width=11,
    length=12,
    depth=13
)


def campaña_en_progreso(session):
    # Campaña en progreso, le falta 1 pledge para estar confirmada
    # 2 pledges minimos, 3 maximos. 1 pledge realizado
    campaign_model = CampaignModel(name='Campaña en progreso',
                                   description='Campaña en progreso. IN_PROGRESS',
                                   campaign_picture_url=None,
                                   printer_id=PRINTER_ID,
                                   pledge_price=5,
                                   end_date=datetime.datetime(2022, 5, 17),
                                   min_pledgers=2,
                                   max_pledgers=3,
                                   status=CampaignStatus.IN_PROGRESS.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model)
    session.flush()

    pledge_model = PledgeModel(campaign_id=campaign_model.id,
                               pledge_price=campaign_model.pledge_price,
                               buyer_id=BUYER_ID,
                               printer_transaction_id=printer_transaction_model.id)
    session.add(pledge_model)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_confirmada_con_1_pledge_faltante(session):
    # Campaña confirmada que le falta 1 pledge para finalizar. Hay cupo maximo
    # 1 pledges minimos, 2 maximos. 1 pledge realizado
    campaign_model = CampaignModel(
        name='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo',
        description='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo. IN_PROGRESS',
        campaign_picture_url=None,
        printer_id=PRINTER_ID,
        pledge_price=5,
        end_date=datetime.datetime(2022, 5, 17),
        min_pledgers=1,
        max_pledgers=2,
        status=CampaignStatus.CONFIRMED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model)
    session.flush()

    pledge_model = PledgeModel(campaign_id=campaign_model.id,
                               pledge_price=campaign_model.pledge_price,
                               buyer_id=BUYER_ID,
                               printer_transaction_id=printer_transaction_model.id)
    session.add(pledge_model)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_confirmada_pero_no_finalizada_y_sin_max_pledgers(session):
    # Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo
    # 1 pledges minimos, sin maximo. 1 pledge realizado.
    campaign_model = CampaignModel(
        name='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo',
        description='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo. IN_PROGRESS',
        campaign_picture_url=None,
        printer_id=PRINTER_ID,
        pledge_price=5,
        end_date=datetime.datetime(2022, 5, 17),
        min_pledgers=1,
        max_pledgers=None,
        status=CampaignStatus.CONFIRMED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model)
    session.flush()

    pledge_model = PledgeModel(
        campaign_id=campaign_model.id,
        pledge_price=campaign_model.pledge_price,
        buyer_id=BUYER_ID,
        printer_transaction_id=printer_transaction_model.id
    )
    session.add(pledge_model)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_completada(session):
    # Campaña completada.
    # 1 pledges minimos, 2 maximos. 2 pledges realizado
    campaign_model = CampaignModel(name='Campaña completada',
                                   description='Campaña completada. COMPLETED',
                                   campaign_picture_url=None,
                                   printer_id=PRINTER_ID,
                                   pledge_price=5,
                                   end_date=datetime.datetime(2021, 4, 4),
                                   min_pledgers=1,
                                   max_pledgers=2,
                                   status=CampaignStatus.COMPLETED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model_1 = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=False
    )
    session.add(printer_transaction_model_1)
    session.flush()

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 printer_transaction_id=printer_transaction_model_1.id)
    session.add(pledge_model_1)
    session.flush()

    printer_transaction_model_2 = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=False
    )
    session.add(printer_transaction_model_2)
    session.flush()

    pledge_model_2 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=ADDITIONAL_BUYER_ID_1,
                                 printer_transaction_id=printer_transaction_model_2.id)
    session.add(pledge_model_2)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()

    order_for_pledge_1_model = OrderModel(
        campaign_id=campaign_model.id,
        pledge_id=pledge_model_1.id,
        buyer_id=pledge_model_1.buyer_id,
        status=OrderStatus.IN_PROGRESS.value
    )
    session.add(order_for_pledge_1_model)
    session.commit()

    order_for_pledge_2_model = OrderModel(
        campaign_id=campaign_model.id,
        pledge_id=pledge_model_2.id,
        buyer_id=pledge_model_2.buyer_id,
        status=OrderStatus.DISPATCHED.value
    )
    session.add(order_for_pledge_2_model)
    session.commit()


def campaña_insatisfecha(session):
    # Campaña insatisfecha que no alcanzo el objetivo por tiempo
    # 6 pledges minimos, 10 maximos. 1 pledges realizado
    campaign_model = CampaignModel(name='Campaña insatisfecha',
                                   description='Campaña insatisfecha. UNSATISFIED',
                                   campaign_picture_url=None,
                                   printer_id=PRINTER_ID,
                                   pledge_price=5,
                                   end_date=datetime.datetime(2021, 4, 4),
                                   min_pledgers=6,
                                   max_pledgers=10,
                                   status=CampaignStatus.UNSATISFIED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model)
    session.flush()

    printer_refund_transaction_model = TransactionModel(
        mp_payment_id=printer_transaction_model.mp_payment_id,
        user_id=printer_transaction_model.user_id,
        amount=printer_transaction_model.amount * -1,
        type=TransactionType.REFUND.value,
        is_future=printer_transaction_model.is_future
    )
    session.add(printer_refund_transaction_model)
    session.flush()

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 deleted_at=datetime.datetime(2021, 4, 4),
                                 printer_transaction_id=printer_transaction_model.id)
    session.add(pledge_model_1)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_que_sera_finalizada(session):
    # Campaña que sera finalizada la proxima vez que corra el cron
    # 1 pledges minimos, 2 maximos. 2 pledges realizado
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

    campaign_model = CampaignModel(name='Campaña a ser finalizada en la fecha {}'.format(tomorrow),
                                   description='Campaña a ser finalizada en la fecha {}. TO_BE_FINALIZED'.format(tomorrow),
                                   campaign_picture_url=None,
                                   printer_id=PRINTER_ID,
                                   pledge_price=5,
                                   end_date=tomorrow,
                                   min_pledgers=1,
                                   max_pledgers=2,
                                   status=CampaignStatus.TO_BE_FINALIZED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model_1 = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model_1)
    session.flush()

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 printer_transaction_id=printer_transaction_model_1.id)
    session.add(pledge_model_1)
    session.flush()

    printer_transaction_model_2 = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model_2)
    session.flush()

    pledge_model_2 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=ADDITIONAL_BUYER_ID_1,
                                 printer_transaction_id=printer_transaction_model_2.id)
    session.add(pledge_model_2)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()

def campaña_cancelada(session):
    # Campaña cancelada
    # 3 pledges minimos, 5 maximos. 1 pledges realizado (que fue borrado)
    campaign_model = CampaignModel(name='Campaña cancelada',
                                   description='Campaña cancelada. CANCELLED',
                                   campaign_picture_url=None,
                                   printer_id=PRINTER_ID,
                                   pledge_price=5,
                                   end_date=datetime.datetime(2021, 4, 4),
                                   min_pledgers=3,
                                   max_pledgers=5,
                                   status=CampaignStatus.CANCELLED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model)
    session.flush()

    printer_refund_transaction_model = TransactionModel(
        mp_payment_id=printer_transaction_model.mp_payment_id,
        user_id=printer_transaction_model.user_id,
        amount=printer_transaction_model.amount  * -1,
        type=TransactionType.REFUND.value,
        is_future=printer_transaction_model.is_future
    )
    session.add(printer_refund_transaction_model)
    session.flush()

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 deleted_at=datetime.datetime(2021, 4, 3),
                                 printer_transaction_id=printer_transaction_model.id)
    session.add(pledge_model_1)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_que_sera_cancelada(session):
    # Campaña que sera cancelada la proxima vez que corra el cron
    # 3 pledges minimos, 5 maximos. 1 pledges realizado
    campaign_model = CampaignModel(name='Campaña a ser cancelada cuando corra el cron',
                                   description='Campaña a ser cancelada cuando corra el cron. TO_BE_CANCELLED',
                                   campaign_picture_url=None,
                                   printer_id=PRINTER_ID,
                                   pledge_price=5,
                                   end_date=datetime.datetime(2022, 4, 4),
                                   min_pledgers=3,
                                   max_pledgers=5,
                                   status=CampaignStatus.TO_BE_CANCELLED.value)
    session.add(campaign_model)
    session.flush()

    preference_id = mercadopago_repository.create_campaign_pledge_preference(
        campaign_model.to_campaign_entity()
    )
    campaign_model.mp_preference_id = preference_id

    printer_transaction_model = TransactionModel(
        mp_payment_id=11111111111,
        user_id=PRINTER_ID,
        amount=campaign_model.pledge_price,
        type=TransactionType.PLEDGE.value,
        is_future=True
    )
    session.add(printer_transaction_model)
    session.flush()

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 printer_transaction_id=printer_transaction_model.id)
    session.add(pledge_model_1)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


if __name__ == '__main__':
    with db_session_factory() as session:
        try:
            #session.execute("""
            #    truncate table tech_details cascade;
            #    truncate table orders cascade;
            #    truncate table failed_to_refund_pledges cascade;
            #    truncate table pledges cascade;
            #    truncate table campaign cascade;
            #""")

            campaña_en_progreso(session)
            campaña_confirmada_pero_no_finalizada_y_sin_max_pledgers(session)
            campaña_confirmada_con_1_pledge_faltante(session)
            campaña_completada(session)
            campaña_insatisfecha(session)
            campaña_que_sera_finalizada(session)
            campaña_que_sera_cancelada(session)
            campaña_cancelada(session)

            session.commit()
        except Exception as ex:
            print(str(ex))
