import copy
import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_app.api.domain import CampaignStatus, OrderStatus
from my_app.api.repositories.models import CampaignModel, PledgeModel, OrderModel, TechDetailsModel

engine = create_engine(os.environ["DATABASE_URL"])
db_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Change with your own printer and buyer account IDs
PRINTER_ID = 1
BUYER_ID = 2

# Buyers IDs (don't use your own)
ADDITIONAL_BUYER_ID_1 = 4
ADDITIONAL_BUYER_ID_2 = 6
ADDITIONAL_BUYER_ID_3 = 8

common_tech_detail_model = TechDetailsModel(
    material="Material",
    weight=10,
    width=11,
    length=12,
    depth=13
)


def campaña_en_progreso(session):
    # Campaña en progreso, le falta 1 pledge para finalizar
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

    pledge_model = PledgeModel(campaign_id=campaign_model.id,
                               pledge_price=campaign_model.pledge_price,
                               buyer_id=BUYER_ID)
    session.add(pledge_model)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_en_progreso_con_objetivo_alcanzado_pero_no_finalizada_y_con_max_pledgers(session):
    # Campaña en progreso con el objetivo alcanzado pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo
    # 1 pledges minimos, 10 maximos. 1 pledge realizado
    campaign_model = CampaignModel(
        name='Campaña en progreso con el objetivo alcanzado pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo',
        description='Campaña en progreso con el objetivo alcanzado pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo. IN_PROGRESS',
        campaign_picture_url=None,
        printer_id=PRINTER_ID,
        pledge_price=5,
        end_date=datetime.datetime(2022, 5, 17),
        min_pledgers=1,
        max_pledgers=10,
        status=CampaignStatus.IN_PROGRESS.value)
    session.add(campaign_model)
    session.flush()

    pledge_model = PledgeModel(campaign_id=campaign_model.id,
                               pledge_price=campaign_model.pledge_price,
                               buyer_id=BUYER_ID)
    session.add(pledge_model)
    session.flush()

    tech_detail_model = copy.deepcopy(common_tech_detail_model)
    tech_detail_model.campaign_id = campaign_model.id
    session.add(tech_detail_model)
    session.flush()


def campaña_en_progreso_con_objetivo_alcanzado_pero_no_finalizada_y_sin_max_pledgers(session):
    # Campaña en progreso con el objetivo alcanzado pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo
    # 1 pledges minimos, sin maximo. 1 pledge realizado.
    campaign_model = CampaignModel(
        name='Campaña en progreso con el objetivo alcanzado pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo',
        description='Campaña en progreso con el objetivo alcanzado pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo. IN_PROGRESS',
        campaign_picture_url=None,
        printer_id=PRINTER_ID,
        pledge_price=5,
        end_date=datetime.datetime(2022, 5, 17),
        min_pledgers=1,
        max_pledgers=None,
        status=CampaignStatus.IN_PROGRESS.value)
    session.add(campaign_model)
    session.flush()

    pledge_model = PledgeModel(
        campaign_id=campaign_model.id,
        pledge_price=campaign_model.pledge_price,
        buyer_id=BUYER_ID)
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

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID)
    session.add(pledge_model_1)
    session.flush()

    pledge_model_2 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=ADDITIONAL_BUYER_ID_1)
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

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 deleted_at=datetime.datetime(2021, 4, 4))
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

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID)
    session.add(pledge_model_1)
    session.flush()

    pledge_model_2 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=ADDITIONAL_BUYER_ID_1)
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

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID,
                                 deleted_at=datetime.datetime(2021, 4, 3))
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

    pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                 pledge_price=campaign_model.pledge_price,
                                 buyer_id=BUYER_ID)
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
            campaña_en_progreso_con_objetivo_alcanzado_pero_no_finalizada_y_sin_max_pledgers(session)
            campaña_en_progreso_con_objetivo_alcanzado_pero_no_finalizada_y_con_max_pledgers(session)
            campaña_completada(session)
            campaña_insatisfecha(session)
            campaña_que_sera_finalizada(session)
            campaña_que_sera_cancelada(session)
            campaña_cancelada(session)

            session.commit()
        except Exception as ex:
            print(str(ex))
