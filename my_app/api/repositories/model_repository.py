import datetime
import uuid
from typing import List, Optional

from sqlalchemy import asc
from sqlalchemy.orm import noload, lazyload

from my_app.api.domain import ModelPrototype, Model, ModelImagePrototype, ModelImage, ModelCategory, \
    ModelLike, ModelPurchase, TransactionType, Page, File
from my_app.api.exceptions import MercadopagoException, ModelCreationException, NotFoundException, BusinessException
from my_app.api.repositories.mercadopago_repository import MercadopagoRepository
from my_app.api.repositories.models import ModelModel, ModelFileModel, ModelImageModel, ModelCategoryModel, \
    ModelLikeModel, TransactionModel, ModelPurchaseModel
from my_app.api.repositories.s3_repository import S3Repository
from my_app.api.repositories.utils import paginate, DEFAULT_PAGE, DEFAULT_PAGE_SIZE, apply_model_filters, \
    apply_model_order

MODEL_CREATION_ERROR = 'Ocurrió un error al crear el modelo'
MODEL_IMAGE_NOT_FOUND = 'La imagen del modelo no existe'
MODEL_NOT_FOUND = "El modelo no existe"
NOT_OWNER = "No puede eliminar un modelo que no le pertenece"


class ModelRepository:
    def __init__(self, db, mercadopago_repository: MercadopagoRepository, s3_repository: S3Repository):
        self.db = db
        self.mercadopago_repository = mercadopago_repository
        self.s3_repository = s3_repository

    def delete_model(self, model_id: int, user_id: int):
        model_model = self._get_model_model_by_id(model_id)

        if model_model is None:
            raise NotFoundException(MODEL_NOT_FOUND)

        if model_model.designer_id != user_id:
            raise BusinessException(NOT_OWNER)

        model_model.deleted_at = datetime.datetime.now()
        self.db.session.commit()

    def create_model(
            self,
            model_prototype: ModelPrototype,
            model_file: File,
            model_image_files: List[File]
    ) -> Model:
        s3_upload_files = []

        try:
            # Create model file
            model_file_name = self._generate_model_file_name()
            model_file_url = self.s3_repository.upload_file(model_file, model_file_name)
            model_file_model = ModelFileModel(
                model_file_url=model_file_url,
                file_name=model_file_name
            )
            s3_upload_files.append(model_file_model)
            self.db.session.add(model_file_model)
            self.db.session.flush()

            # Create model
            model_model = ModelModel(
                designer_id=model_prototype.designer_id,
                name=model_prototype.name,
                description=model_prototype.description,
                model_category_id=model_prototype.model_category_id,
                model_file_id=model_file_model.id,
                likes=0,
                width=model_prototype.width,
                length=model_prototype.length,
                depth=model_prototype.depth,
                allow_purchases=model_prototype.allow_purchases,
                allow_alliances=model_prototype.allow_alliances,
                purchase_price=model_prototype.purchase_price,
                desired_percentage=model_prototype.desired_percentage
            )
            self.db.session.add(model_model)
            self.db.session.flush()

            # Create model preference if purchases are allowed and purchase price was provided
            if model_model.allow_purchases and model_model.purchase_price is not None:
                preference_id = self.mercadopago_repository.create_model_purchase_preference(
                    model_model.to_entity()
                )
                model_model.mp_preference_id = preference_id

            # Create model images
            for model_image_file in model_image_files:
                file_name = self._generate_model_image_name()
                image_url = self.s3_repository.upload_file(model_image_file, file_name)
                s3_upload_files.append(
                    ModelImageModel(
                        model_id=model_model.id,
                        file_name=file_name,
                        model_picture_url=image_url
                    )
                )
            self.db.session.add_all(s3_upload_files)

            self.db.session.commit()

        except MercadopagoException as mpex:
            self.db.session.rollback()
            raise mpex
        except Exception as ex:
            self.db.session.rollback()
            for file in s3_upload_files:
                self.s3_repository.delete_file(file.file_name)
            raise ModelCreationException("{}: {}".format(MODEL_CREATION_ERROR, str(ex)))

        return model_model.to_entity()

    def create_model_image(self, prototype: ModelImagePrototype) -> ModelImage:
        model_image_model = ModelImageModel(
            model_id=prototype.model_id,
            model_picture_url=prototype.model_picture_url,
            file_name=prototype.file_name
        )

        self.db.session.add(model_image_model)
        self.db.session.commit()

        return model_image_model.to_entity()

    def delete_model_image(self, model_image_id: int) -> ModelImage:
        model_image_model = self.db.session.query(ModelImageModel) \
            .filter_by(id=model_image_id) \
            .first()
        if model_image_model is None:
            raise NotFoundException(MODEL_IMAGE_NOT_FOUND)

        self.db.session.delete(model_image_model)
        self.db.session.commit()

        return model_image_model.to_entity()

    def get_model_categories(self) -> (List[ModelCategory]):
        model_categories = self.db.session.query(ModelCategoryModel).all()

        return [mc.to_entity() for mc in model_categories]

    def add_like_to_model(self, model_id: int, user_id: int) -> ModelLike:
        model_model = self._get_model_model_by_id(model_id)
        model_like_model = self._get_model_like_model_by_model_and_user(model_id, user_id)

        if model_like_model is not None:
            return model_like_model.to_entity()

        model_model.likes += 1
        model_like_model = ModelLikeModel(
            model_id=model_id,
            user_id=user_id
        )

        self.db.session.add(model_like_model)
        self.db.session.commit()

        return model_like_model.to_entity()

    def remove_like_from_model(self, model_id: int, user_id: int):
        model_model = self._get_model_model_by_id(model_id)
        model_like_model = self._get_model_like_model_by_model_and_user(model_id, user_id)

        if model_like_model is None:
            return

        if model_like_model.user_id != user_id:
            raise BusinessException("No esta autorizado a realizar esta acción")

        model_model.likes -= 1
        self.db.session.delete(model_like_model)
        self.db.session.commit()

    def create_model_purchase(
            self,
            model_id: int,
            payment_id: int,
            printer_id: int,
    ) -> ModelPurchase:
        try:
            # Retrieve payment data from mercadopago
            payment = self.mercadopago_repository.get_payment_data(payment_id)

            # Retrieve model data
            model_model = self._get_model_model_by_id(model_id)

            # Create model purchase transaction
            model_purchase_transaction_model = TransactionModel(
                mp_payment_id=payment_id,
                user_id=model_model.designer.id,
                amount=payment.get_transaction_net_amount(),
                type=TransactionType.MODEL_PURCHASE.value,
                is_future=False
            )
            self.db.session.add(model_purchase_transaction_model)
            self.db.session.flush()

            model_purchase_model = ModelPurchaseModel(
                printer_id=printer_id,
                model_id=model_id,
                price=model_model.purchase_price,
                transaction_id=model_purchase_transaction_model.id,
                created_at=datetime.datetime.now()
            )
            self.db.session.add(model_purchase_model)

            self.db.session.commit()

            model_purchase_model.model = model_model
        except Exception as exc:
            self.db.session.rollback()
            self.mercadopago_repository.refund_payment(payment_id)
            raise BusinessException("Ocurrió un error al crear la compra del modelo: {}".format(str(exc)))

        return model_purchase_model.to_entity()

    def get_model_detail(self, model_id: int, user_id: Optional[int]) -> Model:
        model_model = self.db.session.query(ModelModel) \
            .filter(ModelModel.id == model_id) \
            .filter(ModelModel.deleted_at == None) \
            .options(noload(ModelModel.model_file)) \
            .first()

        if model_model is None:
            raise NotFoundException(MODEL_NOT_FOUND)

        # If user was provided, check if model was liked by the user or not
        liked_by_user = None
        if user_id is not None:
            liked_by_user = True if self._get_model_like_model_by_model_and_user(model_id, user_id) is not None else False

        return model_model.to_entity(liked_by_user=liked_by_user)

    def get_printer_model_purchases(self, printer_id: int, filters: dict) -> Page[ModelPurchase]:
        query = self.db.session.query(ModelPurchaseModel).join(ModelModel).filter(ModelPurchaseModel.printer_id == printer_id)
        query = apply_model_filters(query, filters)
        query = query.options(noload(ModelPurchaseModel.printer))
        query = apply_model_order(query, filters)

        model_purchase_models = paginate(query, filters).all()

        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=[mpm.to_entity() for mpm in model_purchase_models]
        )

    def get_models(self, filters: dict, user_id: Optional[int]) -> Page[Model]:
        """
        Returns paginated models using filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        user_id: STR
            User who requested the models.
        """
        query = self.db.session.query(ModelModel).filter(ModelModel.deleted_at == None)
        query = apply_model_filters(query, filters)
        query = query.options(noload(ModelModel.model_file))
        query = apply_model_order(query, filters)

        model_models = paginate(query, filters).all()

        # If user was provided, retrieve it's like for these models
        models = []
        if user_id is not None:
            model_likes = self.db.session.query(ModelLikeModel) \
                .filter(ModelLikeModel.user_id == user_id) \
                .filter(ModelLikeModel.model_id.in_([mm.id for mm in model_models])) \
                .all()

            for model_model in model_models:
                is_liked = False
                for model_like in model_likes:
                    if model_model.id == model_like.model_id:
                        is_liked = True
                        break
                models.append(model_model.to_entity(liked_by_user=is_liked))

        else:
            models = [mm.to_entity() for mm in model_models]

        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=models
        )

    def get_designer_models(self, designer_id: int, filters: dict) -> Page[Model]:
        """
        Returns paginated models for designers using filters

        Parameters
        ----------
        filters: dict[str,str]
            Dict with filters to apply.
        designer_id: str
            Designer who requested it's models.
        """
        query = self.db.session.query(ModelModel)\
            .filter(ModelModel.deleted_at == None)\
            .filter(ModelModel.designer_id == designer_id)
        query = apply_model_filters(query, filters)
        query = query.options(noload(ModelModel.model_file))
        query = apply_model_order(query, filters)

        model_models = paginate(query, filters).all()

        total_records = query.count()

        return Page(
            page=filters.get("page", DEFAULT_PAGE),
            page_size=filters.get("page_size", DEFAULT_PAGE_SIZE),
            total_records=total_records,
            data=[mm.to_entity() for mm in model_models]
        )

    def get_model_purchase_from_printer(self, model_id: int, printer_id: int) -> ModelPurchase:
        model_purchase_model = self.db.session.query(ModelPurchaseModel).join(ModelModel) \
            .filter(ModelPurchaseModel.printer_id == printer_id) \
            .filter(ModelPurchaseModel.model_id == model_id) \
            .options(noload(ModelPurchaseModel.printer)) \
            .first()

        if model_purchase_model is None:
            raise NotFoundException("No se encontro la compra del modelo especificado")

        return model_purchase_model.to_entity()

    def get_model_by_id(self, model_id: int) -> Model:
        model_model = self._get_model_model_by_id(model_id)

        if model_model is None:
            raise NotFoundException(MODEL_NOT_FOUND)

        return model_model.to_entity()

    def _get_model_model_by_id(self, model_id: int) -> ModelModel:
        model_model = self.db.session.query(ModelModel) \
            .filter(ModelModel.id == model_id) \
            .filter(ModelModel.deleted_at == None) \
            .first()

        if model_model is None:
            raise NotFoundException(MODEL_NOT_FOUND)

        return model_model

    def _get_model_like_model_by_model_and_user(self, model_id: int, user_id: int) -> Optional[ModelLikeModel]:
        return self.db.session.query(ModelLikeModel) \
            .filter(ModelLikeModel.user_id == user_id) \
            .filter(ModelLikeModel.model_id == model_id) \
            .first()

    def _generate_model_image_name(self) -> str:
        return "model_images/{}".format(uuid.uuid4())

    def _generate_model_file_name(self) -> str:
        return "model_files/{}.stl".format(uuid.uuid4())
