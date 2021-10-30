import urllib.request
import uuid
from concurrent.futures import Executor
from typing import List, Optional

from my_app.api.domain import ModelPrototype, Model, File, ModelImage, ModelImagePrototype, \
    ModelCategory, ModelLike, ModelPurchase, Page, ModelOrdering, ModelOrderingEnum, Campaign
from my_app.api.exceptions import BusinessException
from my_app.api.repositories import ModelRepository, S3Repository, EmailRepository
from my_app.api.utils.email import create_model_purchase_email


class ModelService:
    def __init__(
            self,
            model_repository: ModelRepository,
            s3_repository: S3Repository,
            executor: Executor,
            email_repository: EmailRepository
    ):
        self.model_repository = model_repository
        self.s3_repository = s3_repository
        self.executor = executor
        self.email_repository = email_repository

    def create_model(self, prototype: ModelPrototype, model_file: File, model_image_files: List[File]) -> Model:
        # Validate if model is purchasable
        if prototype.allow_purchases is True:
            if prototype.purchase_price is None:
                raise BusinessException(
                    "Si el modelo esta habilitado para ser comprado, se debe indicar un precio de compra"
                )

        # Validate if model accept alliances
        if prototype.allow_alliances is True:
            if prototype.desired_percentage is None:
                raise BusinessException(
                    "Si el modelo acepta alianzas, se debe indicar el porcentaje de ganancias deseado"
                )
            if prototype.desired_percentage > 50:
                raise BusinessException(
                    "El porcentaje por alianza no puede ser mayor al 50%"
                )

        return self.model_repository.create_model(prototype, model_file, model_image_files)

    def create_model_image(self, model_id: int, image: File) -> ModelImage:
        file_name = self._generate_model_image_name()
        image_url = self.s3_repository.upload_file(image, file_name)

        model_image_prototype = ModelImagePrototype(
            model_id=model_id,
            file_name=file_name,
            model_picture_url=image_url
        )

        return self.model_repository.create_model_image(model_image_prototype)

    def delete_model_image(self, model_image_id: int):
        deleted_model_image = self.model_repository.delete_model_image(model_image_id)
        self.s3_repository.delete_file(deleted_model_image.file_name)

    def get_model_categories(self) -> (List[ModelCategory]):
        return self.model_repository.get_model_categories()

    def add_like_to_model(self, model_id: int, user_id: int) -> ModelLike:
        return self.model_repository.add_like_to_model(model_id, user_id)

    def remove_like_from_model(self, model_id: int, user_id: int):
        self.model_repository.remove_like_from_model(model_id, user_id)

    def create_model_purchase(self, model_id: int, payment_id: int, printer_id: int) -> ModelPurchase:
        model_purchase = self.model_repository.create_model_purchase(model_id, payment_id, printer_id)

        # Send email to designer
        self.executor.submit(
            self.email_repository.send_individual_email,
            create_model_purchase_email(model_purchase.model.designer.email, model_purchase.model)
        )

        return model_purchase

    def get_printer_model_purchases(self, printer_id: int, filters: dict) -> Page[ModelPurchase]:
        return self.model_repository.get_printer_model_purchases(printer_id, filters)

    def get_model_detail(self, model_id: int, user_id: Optional[int]) -> Model:
        return self.model_repository.get_model_detail(model_id, user_id)

    def get_models(self, filters: dict, user_id: Optional[int]) -> Page[Model]:
        return self.model_repository.get_models(filters, user_id)

    def get_model_ordering(self) -> List[ModelOrdering]:
        return [ModelOrdering(moe.value, moe.name) for moe in ModelOrderingEnum]

    def get_designer_models(self, designer_id: int, filters: dict) -> Page[Model]:
        return self.model_repository.get_designer_models(designer_id, filters)

    def delete_model(self, model_id: int, user_id: int):
        self.model_repository.delete_model(model_id, user_id)

    def get_model_purchase_from_printer(self, model_id: int, printer_id: int) -> ModelPurchase:
        return self.model_repository.get_model_purchase_from_printer(model_id, printer_id)

    def get_model_current_campaigns(self, model_id: int) -> List[Campaign]:
        return self.model_repository.get_model_current_campaigns(model_id)

    def get_model_image_data(self, model_id:int) -> bytes:
        model = self.model_repository.get_model_by_id(model_id)

        with urllib.request.urlopen(model.model_file.model_file_url) as response:
            image_data = response.read()

        return image_data

    def _generate_model_image_name(self) -> str:
        return "model_images/{}".format(uuid.uuid4())
