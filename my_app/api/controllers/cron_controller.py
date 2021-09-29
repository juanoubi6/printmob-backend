import copy
import datetime

from flask import request

from concurrent.futures import Executor

from sqlalchemy.orm import sessionmaker

from my_app.api.domain import UserType, CampaignStatus, OrderStatus, TransactionType
from my_app.api.repositories import EmailRepository
from my_app.api.repositories.models import UserModel, BankInformationModel, PrinterModel, AddressModel, BuyerModel, \
    CampaignModel, TransactionModel, PledgeModel, TechDetailsModel, OrderModel, \
    ModelCategoryModel, DesignerModel, ModelFileModel, ModelModel, ModelLikeModel, ModelImageModel, ModelPurchaseModel
from my_app.crons import finalize_campaign
from my_app.crons.cancel_campaigns import cancel_campaigns

common_tech_detail_model = TechDetailsModel(
    material="Material",
    weight=10,
    width=11,
    length=12,
    depth=13
)


class CronController:
    def __init__(self,
                 session_factory: sessionmaker,
                 email_repository: EmailRepository,
                 executor: Executor,
                 mercadopago_repository
                 ):
        self.session_factory = session_factory
        self.email_repository = email_repository
        self.executor = executor
        self.mercadopago_repository = mercadopago_repository

        # Change with your own printer and buyer account IDs
        self.PRINTER_ID = None
        self.BUYER_ID = None
        self.DESIGNER_ID = None

        # Buyers IDs (don't use your own)
        self.ADDITIONAL_BUYER_ID_1 = None
        self.ADDITIONAL_BUYER_ID_2 = None
        self.ADDITIONAL_BUYER_ID_3 = None

    def finish_campaigns(self):
        finalize_campaign(self.session_factory, self.email_repository, self.executor,
                          self.mercadopago_repository)

    def cancel_campaigns(self):
        cancel_campaigns(self.session_factory, self.email_repository, self.executor,
                         self.mercadopago_repository)

    def end_campaigns(self) -> (dict, int):
        self.finish_campaigns()
        self.cancel_campaigns()

        return {"result": "done"}, 200

    def in_progress_campaign(self, session):
        # Campaña en progreso, le falta 1 pledge para estar confirmada
        # 2 pledges minimos, 3 maximos. 1 pledge realizado
        campaign_model = CampaignModel(name='Campaña en progreso',
                                       description='Campaña en progreso. IN_PROGRESS',
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=datetime.datetime(2022, 5, 17),
                                       min_pledgers=2,
                                       max_pledgers=3,
                                       status=CampaignStatus.IN_PROGRESS.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model)
        session.flush()

        pledge_model = PledgeModel(campaign_id=campaign_model.id,
                                   pledge_price=campaign_model.pledge_price,
                                   buyer_id=self.BUYER_ID,
                                   printer_transaction_id=printer_transaction_model.id)
        session.add(pledge_model)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def in_progress_wont_confirm_campaign(self, session):
        # Campaña en progreso, le falta 1 pledge para estar confirmada
        # 2 pledges minimos, 3 maximos. 1 pledge realizado
        campaign_model = CampaignModel(name='Campaña en progreso',
                                       description='Campaña en progreso pero no llega a sus pledges. Va a ser UNSATISFIED',
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=datetime.datetime.now() + datetime.timedelta(days=1),
                                       min_pledgers=2,
                                       max_pledgers=3,
                                       status=CampaignStatus.IN_PROGRESS.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model)
        session.flush()

        pledge_model = PledgeModel(campaign_id=campaign_model.id,
                                   pledge_price=campaign_model.pledge_price,
                                   buyer_id=self.BUYER_ID,
                                   printer_transaction_id=printer_transaction_model.id)
        session.add(pledge_model)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def confirmed_1_pledge_left_campaign(self, session):
        # Campaña confirmada que le falta 1 pledge para finalizar. Hay cupo maximo
        # 1 pledges minimos, 2 maximos. 1 pledge realizado
        campaign_model = CampaignModel(
            name='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo',
            description='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. Hay cupo maximo. IN_PROGRESS',
            campaign_picture_url=None,
            printer_id=self.PRINTER_ID,
            pledge_price=5,
            end_date=datetime.datetime(2022, 5, 17),
            min_pledgers=1,
            max_pledgers=2,
            status=CampaignStatus.CONFIRMED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model)
        session.flush()

        pledge_model = PledgeModel(campaign_id=campaign_model.id,
                                   pledge_price=campaign_model.pledge_price,
                                   buyer_id=self.BUYER_ID,
                                   printer_transaction_id=printer_transaction_model.id)
        session.add(pledge_model)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def confirmed_but_not_finalized_campaign_without_max_pledges_campaign(self, session):
        # Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo
        # 1 pledges minimos, sin maximo. 1 pledge realizado.
        campaign_model = CampaignModel(
            name='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo',
            description='Campaña confirmada pero que aun no alcanzo la fecha de finalizacion. No hay cupo maximo. IN_PROGRESS',
            campaign_picture_url=None,
            printer_id=self.PRINTER_ID,
            pledge_price=5,
            end_date=datetime.datetime(2022, 5, 17),
            min_pledgers=1,
            max_pledgers=None,
            status=CampaignStatus.CONFIRMED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model)
        session.flush()

        pledge_model = PledgeModel(
            campaign_id=campaign_model.id,
            pledge_price=campaign_model.pledge_price,
            buyer_id=self.BUYER_ID,
            printer_transaction_id=printer_transaction_model.id
        )
        session.add(pledge_model)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def completed_campaign(self, session):
        # Campaña completada.
        # 1 pledges minimos, 2 maximos. 2 pledges realizado
        campaign_model = CampaignModel(name='Campaña completada',
                                       description='Campaña completada. COMPLETED',
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=datetime.datetime(2021, 4, 4),
                                       min_pledgers=1,
                                       max_pledgers=2,
                                       status=CampaignStatus.COMPLETED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model_1 = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=False
        )
        session.add(printer_transaction_model_1)
        session.flush()

        pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                     pledge_price=campaign_model.pledge_price,
                                     buyer_id=self.BUYER_ID,
                                     printer_transaction_id=printer_transaction_model_1.id)
        session.add(pledge_model_1)
        session.flush()

        printer_transaction_model_2 = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=False
        )
        session.add(printer_transaction_model_2)
        session.flush()

        pledge_model_2 = PledgeModel(campaign_id=campaign_model.id,
                                     pledge_price=campaign_model.pledge_price,
                                     buyer_id=self.ADDITIONAL_BUYER_ID_1,
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
        session.flush()

        order_for_pledge_2_model = OrderModel(
            campaign_id=campaign_model.id,
            pledge_id=pledge_model_2.id,
            buyer_id=pledge_model_2.buyer_id,
            status=OrderStatus.DISPATCHED.value
        )
        session.add(order_for_pledge_2_model)
        session.flush()

        return campaign_model

    def unsatisfied_campaign(self, session):
        # Campaña insatisfecha que no alcanzo el objetivo por tiempo
        # 6 pledges minimos, 10 maximos. 1 pledges realizado
        campaign_model = CampaignModel(name='Campaña insatisfecha',
                                       description='Campaña insatisfecha. UNSATISFIED',
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=datetime.datetime(2021, 4, 4),
                                       min_pledgers=6,
                                       max_pledgers=10,
                                       status=CampaignStatus.UNSATISFIED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
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
                                     buyer_id=self.BUYER_ID,
                                     deleted_at=datetime.datetime(2021, 4, 4),
                                     printer_transaction_id=printer_transaction_model.id)
        session.add(pledge_model_1)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def will_be_finalized_campaign(self, session):
        # Campaña que sera finalizada la proxima vez que corra el cron
        # 1 pledges minimos, 2 maximos. 2 pledges realizado
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        campaign_model = CampaignModel(name='Campaña a ser finalizada en la fecha {}'.format(yesterday),
                                       description='Campaña a ser finalizada en la fecha {}. TO_BE_FINALIZED'.format(
                                           yesterday),
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=yesterday,
                                       min_pledgers=1,
                                       max_pledgers=2,
                                       status=CampaignStatus.TO_BE_FINALIZED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model_1 = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model_1)
        session.flush()

        pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                     pledge_price=campaign_model.pledge_price,
                                     buyer_id=self.BUYER_ID,
                                     printer_transaction_id=printer_transaction_model_1.id)
        session.add(pledge_model_1)
        session.flush()

        printer_transaction_model_2 = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model_2)
        session.flush()

        pledge_model_2 = PledgeModel(campaign_id=campaign_model.id,
                                     pledge_price=campaign_model.pledge_price,
                                     buyer_id=self.ADDITIONAL_BUYER_ID_1,
                                     printer_transaction_id=printer_transaction_model_2.id)
        session.add(pledge_model_2)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def canceled_campaign(self, session):
        # Campaña cancelada
        # 3 pledges minimos, 5 maximos. 1 pledges realizado (que fue borrado)
        campaign_model = CampaignModel(name='Campaña cancelada',
                                       description='Campaña cancelada. CANCELLED',
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=datetime.datetime(2021, 4, 4),
                                       min_pledgers=3,
                                       max_pledgers=5,
                                       status=CampaignStatus.CANCELLED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
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
                                     buyer_id=self.BUYER_ID,
                                     deleted_at=datetime.datetime(2021, 4, 3),
                                     printer_transaction_id=printer_transaction_model.id)
        session.add(pledge_model_1)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def will_be_cancelled_campaign(self, session):
        # Campaña que sera cancelada la proxima vez que corra el cron
        # 3 pledges minimos, 5 maximos. 1 pledges realizado
        campaign_model = CampaignModel(name='Campaña a ser cancelada cuando corra el cron',
                                       description='Campaña a ser cancelada cuando corra el cron. TO_BE_CANCELLED',
                                       campaign_picture_url=None,
                                       printer_id=self.PRINTER_ID,
                                       pledge_price=5,
                                       end_date=datetime.datetime(2022, 4, 4),
                                       min_pledgers=3,
                                       max_pledgers=5,
                                       status=CampaignStatus.TO_BE_CANCELLED.value)
        session.add(campaign_model)
        session.flush()

        preference_id = self.mercadopago_repository.create_campaign_pledge_preference(
            campaign_model.to_campaign_entity()
        )
        campaign_model.mp_preference_id = preference_id

        printer_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=self.PRINTER_ID,
            amount=campaign_model.pledge_price,
            type=TransactionType.PLEDGE.value,
            is_future=True
        )
        session.add(printer_transaction_model)
        session.flush()

        pledge_model_1 = PledgeModel(campaign_id=campaign_model.id,
                                     pledge_price=campaign_model.pledge_price,
                                     buyer_id=self.BUYER_ID,
                                     printer_transaction_id=printer_transaction_model.id)
        session.add(pledge_model_1)
        session.flush()

        tech_detail_model = copy.deepcopy(common_tech_detail_model)
        tech_detail_model.campaign_id = campaign_model.id
        session.add(tech_detail_model)
        session.flush()

        return campaign_model

    def modelo_likeado_y_comprado_que_admite_compra_por_precio_fijo_y_porcentaje(self, session, model_category):
        # Modelo
        model_file_model = ModelFileModel(
            model_file_url="https://printmob-dev.s3.us-east-2.amazonaws.com/model_files/5a0ae0f9-e270-41ca-a600-4ab017a753bc.stl",
            file_name="model_files/5a0ae0f9-e270-41ca-a600-4ab017a753bc.stl"
        )
        session.add(model_file_model)
        session.flush()

        model_model = ModelModel(
            designer_id=self.DESIGNER_ID,
            name="Modelo con 2 likes",
            description="Un modelo con 2 likes",
            model_category_id=model_category.id,
            model_file_id=model_file_model.id,
            likes=2,
            width=100,
            length=100,
            depth=100,
            allow_purchases=True,
            allow_alliances=True,
            purchase_price=5.5,
            desired_percentage=20,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            deleted_at=None
        )
        session.add(model_model)
        session.flush()

        # Add preference
        preference_id = self.mercadopago_repository.create_model_purchase_preference(
            model_model.to_entity()
        )
        model_model.mp_preference_id = preference_id

        model_like_1 = ModelLikeModel(
            model_id=model_model.id,
            user_id=self.PRINTER_ID
        )
        model_like_2 = ModelLikeModel(
            model_id=model_model.id,
            user_id=self.BUYER_ID
        )
        session.add_all([model_like_1, model_like_2])
        session.flush()

        # Compra del modelo
        model_purchase_transaction_model = TransactionModel(
            mp_payment_id=11111111111,
            user_id=model_model.designer.id,
            amount=model_model.purchase_price,
            type=TransactionType.MODEL_PURCHASE.value,
            is_future=False
        )
        session.add(model_purchase_transaction_model)
        session.flush()

        model_purchase_model = ModelPurchaseModel(
            printer_id=self.PRINTER_ID,
            model_id=model_model.id,
            price=model_purchase_transaction_model.amount,
            transaction_id=model_purchase_transaction_model.id,
            created_at=datetime.datetime.now()
        )
        session.add(model_purchase_model)
        session.flush()

    def truncate_tables(self):
        with self.session_factory() as session:
            session.execute('TRUNCATE addresses CASCADE;')
            session.execute('TRUNCATE balance_requests CASCADE;')
            session.execute('TRUNCATE bank_information CASCADE;')
            session.execute('TRUNCATE buyers CASCADE;')
            session.execute('TRUNCATE campaign CASCADE;')
            session.execute('TRUNCATE campaign_model_images CASCADE;')
            session.execute('TRUNCATE designers CASCADE;')
            session.execute('TRUNCATE failed_to_refund_pledges CASCADE;')
            session.execute('TRUNCATE model_categories CASCADE;')
            session.execute('TRUNCATE model_files CASCADE;')
            session.execute('TRUNCATE model_images CASCADE;')
            session.execute('TRUNCATE model_likes CASCADE;')
            session.execute('TRUNCATE model_purchases CASCADE;')
            session.execute('TRUNCATE models CASCADE;')
            session.execute('TRUNCATE orders CASCADE;')
            session.execute('TRUNCATE pledges CASCADE;')
            session.execute('TRUNCATE printers CASCADE;')
            session.execute('TRUNCATE tech_details CASCADE;')
            session.execute('TRUNCATE transactions CASCADE;')
            session.execute('TRUNCATE users CASCADE;')
            session.commit()

    def create_test_data(self, req: request) -> (dict, int):
        params = req.args
        if params.get('truncate'):
            self.truncate_tables()

        with self.session_factory() as session:
            # Model categories
            category_arquitectura = ModelCategoryModel(name="Arquitectura")
            category_vehiculos = ModelCategoryModel(name="Vehículos")
            category_figuras_de_accion = ModelCategoryModel(name="Figuras de acción")
            category_accesorios = ModelCategoryModel(name="Accesorios")
            category_hogar = ModelCategoryModel(name="Hogar")
            category_electronica = ModelCategoryModel(name="Electrónica")
            category_repuestos = ModelCategoryModel(name="Repuestos")
            category_protesis = ModelCategoryModel(name="Prótesis")
            category_plantas = ModelCategoryModel(name="Plantas")
            category_deportes = ModelCategoryModel(name="Deportes")
            category_otros = ModelCategoryModel(name="Otros")

            session.add_all([
                category_arquitectura,
                category_vehiculos,
                category_figuras_de_accion,
                category_accesorios,
                category_hogar,
                category_electronica,
                category_repuestos,
                category_protesis,
                category_plantas,
                category_deportes,
                category_otros
            ])
            session.flush()

            # Address
            address_model = AddressModel(
                address="Calle falsa 123",
                zip_code="C1425",
                province="CABA",
                city="CABA",
                floor="7",
                apartment="A"
            )
            session.add(address_model)
            session.flush()

            # Bank information
            bank_information_model = BankInformationModel(
                cbu="2222222222333333333344",
                alias="Alias",
                bank="Banco galicia",
                account_number="123456-78"
            )
            session.add(bank_information_model)
            session.flush()

            # Oubi
            juanma_printer_user_model = UserModel(first_name='Juanma',
                                           last_name='Oubina',
                                           user_name='juanmaprinter',
                                           date_of_birth=datetime.datetime.now(),
                                           email='juan.manuel.oubina@gmail.com',
                                           user_type=UserType.PRINTER.value)
            session.add(juanma_printer_user_model)
            session.flush()

            juanma_buyer_user_model = UserModel(first_name='Juanma',
                                           last_name='Oubina',
                                           user_name='juanmabuyer',
                                           date_of_birth=datetime.datetime.now(),
                                           email='joubina@frba.utn.edu.ar',
                                           user_type=UserType.BUYER.value)
            session.add(juanma_buyer_user_model)
            session.flush()

            juanma_printer_model = PrinterModel(id=juanma_printer_user_model.id, bank_information_id=bank_information_model.id)
            session.add(juanma_printer_model)
            session.flush()

            juanma_buyer_model = BuyerModel(id=juanma_buyer_user_model.id, address_id=address_model.id)
            session.add(juanma_buyer_model)
            session.flush()

            # Axel
            axel_printer_user = UserModel(first_name='Axel',
                                          last_name='Furlan',
                                          user_name='axelprinter',
                                          date_of_birth=datetime.datetime.now(),
                                          email='axel.furlan95@gmail.com',
                                          user_type=UserType.PRINTER.value)
            session.add(axel_printer_user)
            session.flush()

            axel_printer = PrinterModel(id=axel_printer_user.id, bank_information_id=bank_information_model.id)
            session.add(axel_printer)
            session.flush()

            axel_buyer_model = UserModel(first_name='Axel',
                                         last_name='Furlan',
                                         user_name='axelbuyer',
                                         date_of_birth=datetime.datetime.now(),
                                         email='afurlanfigueroa@frba.utn.edu.ar',
                                         user_type=UserType.BUYER.value)
            session.add(axel_buyer_model)
            session.flush()

            axel_buyer = BuyerModel(id=axel_buyer_model.id, address_id=address_model.id)
            session.add(axel_buyer)
            session.flush()

            # Joaco
            joaco_printer_user = UserModel(first_name='Joaquin',
                                           last_name='Leon',
                                           user_name='joacoprinter',
                                           date_of_birth=datetime.datetime.now(),
                                           email='leonjoaquin77@gmail.com',
                                           user_type=UserType.PRINTER.value)
            session.add(joaco_printer_user)
            session.flush()

            joaco_printer = PrinterModel(id=joaco_printer_user.id, bank_information_id=bank_information_model.id)
            session.add(joaco_printer)
            session.flush()

            joaco_buyer_model = UserModel(first_name='Joaquin',
                                          last_name='Leon',
                                          user_name='joacobuyer',
                                          date_of_birth=datetime.datetime.now(),
                                          email='jleon@frba.utn.edu.ar',
                                          user_type=UserType.BUYER.value)
            session.add(joaco_buyer_model)
            session.flush()

            joaco_buyer = BuyerModel(id=joaco_buyer_model.id, address_id=address_model.id)
            session.add(joaco_buyer)
            session.flush()

            # Lucas
            lucas_printer_user = UserModel(first_name='Lucas',
                                           last_name='Costas',
                                           user_name='lucasprinter',
                                           date_of_birth=datetime.datetime.now(),
                                           email='lucascostasutn@gmail.com',
                                           user_type=UserType.PRINTER.value)
            session.add(lucas_printer_user)
            session.flush()

            lucas_printer = PrinterModel(id=lucas_printer_user.id, bank_information_id=bank_information_model.id)
            session.add(lucas_printer)
            session.flush()

            lucas_buyer_model = UserModel(first_name='Lucas',
                                          last_name='Costas',
                                          user_name='lucasbuyer',
                                          date_of_birth=datetime.datetime.now(),
                                          email='lucas.costas@mercadolibre.com',
                                          user_type=UserType.BUYER.value)
            session.add(lucas_buyer_model)
            session.flush()

            lucas_buyer = BuyerModel(id=lucas_buyer_model.id, address_id=address_model.id)
            session.add(lucas_buyer)
            session.flush()

            # Pedro
            pedro_printer_user = UserModel(first_name='Pedro',
                                           last_name='Droven',
                                           user_name='pedroprinter',
                                           date_of_birth=datetime.datetime.now(),
                                           email='pdroven@gmail.com',
                                           user_type=UserType.PRINTER.value)
            session.add(pedro_printer_user)
            session.flush()

            pedro_printer = PrinterModel(id=pedro_printer_user.id, bank_information_id=bank_information_model.id)
            session.add(pedro_printer)
            session.flush()

            pedro_buyer_model = UserModel(first_name='Pedro',
                                          last_name='Droven',
                                          user_name='pedrobuyer',
                                          date_of_birth=datetime.datetime.now(),
                                          email='pdroven@frba.utn.edu.ar',
                                          user_type=UserType.BUYER.value)
            session.add(pedro_buyer_model)
            session.flush()

            pedro_buyer = BuyerModel(id=pedro_buyer_model.id, address_id=address_model.id)
            session.add(pedro_buyer)
            session.flush()

            # Designer user
            printmob_designer_user = UserModel(first_name='Printmob Name',
                                               last_name='Printmob Last Name',
                                               user_name='printmob-designer',
                                               date_of_birth=datetime.datetime.now(),
                                               email='printmobarg@gmail.com',
                                               user_type=UserType.DESIGNER.value)
            session.add(printmob_designer_user)
            session.flush()

            printmob_designer = DesignerModel(id=printmob_designer_user.id, bank_information_id=bank_information_model.id)
            session.add(printmob_designer)
            session.flush()

            # Change with your own printer and buyer account IDs
            self.PRINTER_ID = juanma_printer_model.id
            self.BUYER_ID = juanma_buyer_model.id
            self.DESIGNER_ID = printmob_designer.id

            # Buyers IDs (don't use your own)
            self.ADDITIONAL_BUYER_ID_1 = axel_buyer_model.id
            self.ADDITIONAL_BUYER_ID_2 = lucas_buyer_model.id
            self.ADDITIONAL_BUYER_ID_3 = pedro_buyer_model.id

            # Campaigns
            in_progress_camp = self.in_progress_campaign(session)
            in_progress_wont_confirm_campaign = self.in_progress_wont_confirm_campaign(session)
            confirmed_not_finished_camp = self.confirmed_but_not_finalized_campaign_without_max_pledges_campaign(session)
            confirmed_1_pledge_left_camp = self.confirmed_1_pledge_left_campaign(session)
            completed_camp = self.completed_campaign(session)
            unsatisfied_camp = self.unsatisfied_campaign(session)
            will_be_finalized_camp = self.will_be_finalized_campaign(session)
            will_be_cancelled_camp = self.will_be_cancelled_campaign(session)
            canceled_camp = self.canceled_campaign(session)

            created_campaigns = {
                'in_progress': in_progress_camp.to_campaign_entity().to_json(),
                'in_progress_wont_confirm_campaign': in_progress_wont_confirm_campaign.to_campaign_entity().to_json(),
                'confirmed_not_finished': confirmed_not_finished_camp.to_campaign_entity().to_json(),
                'confirmed_1_pledge_left': confirmed_1_pledge_left_camp.to_campaign_entity().to_json(),
                'completed': completed_camp.to_campaign_entity().to_json(),
                'unsatisfied': unsatisfied_camp.to_campaign_entity().to_json(),
                'will_finish': will_be_finalized_camp.to_campaign_entity().to_json(),
                'will_cancel': will_be_cancelled_camp.to_campaign_entity().to_json(),
                'canceled': canceled_camp.to_campaign_entity().to_json()
            }

            #Diseños
            self.modelo_likeado_y_comprado_que_admite_compra_por_precio_fijo_y_porcentaje(session, category_arquitectura)

            session.commit()

        return {"status":"ok", "created_campaigns": created_campaigns}, 200
