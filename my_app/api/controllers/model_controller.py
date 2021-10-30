import json
from typing import List, Optional

from flask import request

from my_app.api.controllers.validators import validate_model_file_upload, validate_image_upload, \
    validate_pagination_filters, validate_image_file
from my_app.api.domain import Model, UserType, ModelPrototype, File, ModelImage, ModelCategory, ModelLike, \
    ModelPurchase, Page, ModelOrdering, Campaign
from my_app.api.exceptions import BusinessException
from my_app.api.services import ModelService

ONLY_DESIGNERS_ERROR = "Solo los diseñadores pueden crear modelos"
ONLY_PRINTER_ERROR = "Solo los impresores pueden acceder a esta información"
ONLY_DESIGNER_ERROR = "Solo los diseñadores pueden acceder a esta información"


class ModelController:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def create_model(self, req: request, user_data: dict) -> (Model, int):
        if user_data["user_type"] != UserType.DESIGNER.value:
            raise BusinessException(ONLY_DESIGNERS_ERROR)

        prototype = ModelPrototype(
            name=request.form["name"],
            description=request.form["description"],
            model_category_id=int(request.form["model_category_id"]),
            width=int(request.form["width"]),
            length=int(request.form["length"]),
            depth=int(request.form["depth"]),
            allow_purchases=bool(self._str_to_bool(request.form["allow_purchases"])),
            allow_alliances=bool(self._str_to_bool(request.form["allow_alliances"])),
            purchase_price=float(
                request.form["purchase_price"]
            ) if request.form.get("purchase_price", None) is not None else None,
            desired_percentage=float(
                request.form["desired_percentage"]
            ) if request.form.get("desired_percentage", None) is not None else None,
            model_images_urls=[],
            designer_id=int(user_data["id"]),
        )

        # Retrieve and validate model file
        validate_model_file_upload(req.files, 'model_file')
        model_file_data = req.files['model_file']
        model_file = File(content=model_file_data.stream.read(), mimetype=model_file_data.mimetype)

        # Retrieve and validate model images (if provided)
        image_files_data = req.files.getlist("image[]")
        for image_file_data in image_files_data:
            validate_image_file(image_file_data)
        model_image_files = [File(content=mi.stream.read(), mimetype=mi.mimetype) for mi in image_files_data]

        if len(model_image_files) == 0:
            raise BusinessException("Debe subir al menos una imagen de su modelo")

        created_model = self.model_service.create_model(prototype, model_file, model_image_files)

        return created_model.to_json(), 201

    def create_model_image(self, req: request, model_id: int, user_data: dict) -> (ModelImage, int):
        validate_image_upload(req.files, 'image')
        image_data = req.files['image']
        file = File(content=image_data.stream.read(), mimetype=image_data.mimetype)

        model_image = self.model_service.create_model_image(model_id, file)

        return model_image.to_json(), 201

    def delete_model_image(self, req: request, model_id: int, model_image_id: int, user_data: dict) -> (dict, int):
        self.model_service.delete_model_image(model_image_id)

        return {"status": "ok"}, 200

    def get_model_categories(self, req: request) -> (List[ModelCategory], int):
        model_categories = self.model_service.get_model_categories()

        return [mc.to_json() for mc in model_categories], 200

    def add_like_to_model(self, req: request, model_id: int, user_data: dict) -> (ModelLike, int):
        model_like = self.model_service.add_like_to_model(model_id, int(user_data["id"]))

        return model_like.to_json(), 201

    def remove_like_from_model(self, req: request, model_id: int, user_data: dict) -> (dict, int):
        self.model_service.remove_like_from_model(model_id, int(user_data["id"]))

        return {"status": "ok"}, 200

    def create_model_purchase(self, req: request, user_data: dict) -> (ModelPurchase, int):
        body = json.loads(req.data)
        model_id = body.get("model_id", None)
        payment_id = body.get("mp_payment_id", None)

        if model_id is None:
            raise BusinessException("El ID del modelo no fue provisto")

        if payment_id is None:
            raise BusinessException("El ID del pago no fue provisto")

        model_purchase = self.model_service.create_model_purchase(
            model_id=int(model_id),
            payment_id=int(payment_id),
            printer_id=int(user_data["id"])
        )

        return model_purchase.to_json(), 201

    def get_printer_model_purchase(self, req: request, user_data: dict) -> (Page[ModelPurchase], int):
        if user_data["user_type"] != UserType.PRINTER.value:
            raise BusinessException(ONLY_PRINTER_ERROR)

        filters = req.args
        validate_pagination_filters(filters)

        model_purchase_page = self.model_service.get_printer_model_purchases(int(user_data["id"]), filters)

        return model_purchase_page.to_json(), 200

    def get_model_detail(self, req: request, model_id: int, user_data: Optional[dict]) -> (Model, int):
        user_id = int(user_data["id"]) if user_data is not None else None
        model_detail = self.model_service.get_model_detail(model_id, user_id)

        return model_detail.to_json(), 200

    def get_models(self, req: request, user_data: Optional[dict]) -> (Page[Model], int):
        user_id = int(user_data["id"]) if user_data is not None else None

        filters = req.args
        validate_pagination_filters(filters)
        models_page = self.model_service.get_models(filters, user_id)

        return models_page.to_json(), 200

    def get_model_ordering(self, req: request) -> (List[ModelOrdering], int):
        model_orderings = self.model_service.get_model_ordering()

        return [mo.to_json() for mo in model_orderings], 200

    def get_designer_models(self, req: request, designer_id: int, user_data: dict) -> (Page[Model], int):
        if int(user_data["id"]) != designer_id:
            raise BusinessException(ONLY_DESIGNER_ERROR)

        filters = req.args
        validate_pagination_filters(filters)
        models_page = self.model_service.get_designer_models(designer_id, filters)

        return models_page.to_json(), 200

    def delete_model(self, req: request, model_id: int, user_data: dict) -> (dict, int):
        self.model_service.delete_model(model_id, int(user_data["id"]))

        return {"status": "ok"}, 200

    def get_model_purchase_from_printer(self, req: request, model_id: int, user_data: dict) -> (ModelPurchase, int):
        if user_data["user_type"] != UserType.PRINTER.value:
            raise BusinessException(ONLY_PRINTER_ERROR)

        model_purchase = self.model_service.get_model_purchase_from_printer(model_id, int(user_data["id"]))

        return model_purchase.to_json(), 200

    def get_model_image_data(self, req: request):
        model_id = req.args.get("model_id")

        return self.model_service.get_model_image_data(model_id)

    def get_model_current_campaigns(self, req: request, model_id: int) -> (List[Campaign], int):
        campaign_list = self.model_service.get_model_current_campaigns(model_id)

        return [campaign.to_reduced_json() for campaign in campaign_list], 200

    def _str_to_bool(self, str_bool):
        return str_bool.lower() in ("True", "true", "t", "1")
