import datetime

from my_app.api.domain.campaign import CampaignPrototype, CampaignWithModelPrototype
from my_app.api.domain.tech_detail import TechDetailPrototype
from my_app.api.exceptions import InvalidParamException

PAGE_FILTER_NAME = "page"
PAGE_SIZE_FILTER_NAME = "page_size"
VALID_IMAGE_MIMETYPES = ['image/jpeg', "image/png"]
VALID_MODEL_FILE_MIMETYPES = ['application/sla', 'model/stl', 'application/vnd.ms-pki.stl', 'application/x-navistyle',
                              'application/octet-stream']


def validate_pagination_filters(filters: dict):
    if PAGE_FILTER_NAME in filters:
        page_filter = filters[PAGE_FILTER_NAME]
        if (not page_filter.isnumeric()) or (int(page_filter) < 1):
            raise InvalidParamException("El query param 'page' debe ser un número")

    if PAGE_SIZE_FILTER_NAME in filters:
        page_size_filter = filters[PAGE_SIZE_FILTER_NAME]
        if (not page_size_filter.isnumeric()) or (int(page_size_filter) < 1):
            raise InvalidParamException("El query param 'page_size' debe ser un número")


def validate_campaign_prototype(campaign_prototype: CampaignPrototype):
    validate_alphanumeric_field(campaign_prototype.name, "nombre de campaña")
    for image_url in campaign_prototype.campaign_model_image_urls:
        validate_url_field(image_url, "URL de la imagen de la campaña")
    validate_positive_integer_field(campaign_prototype.printer_id, "ID del impresor")
    validate_positive_decimal_field(campaign_prototype.pledge_price, "precio de la reserva")
    validate_campaign_pledgers_interval(campaign_prototype.min_pledgers, campaign_prototype.max_pledgers)
    validate_tech_detail_prototype(campaign_prototype.tech_details)
    validate_future_date(campaign_prototype.end_date)

def validate_campaign_with_model_prototype(campaign_with_model_prototype: CampaignWithModelPrototype):
    validate_alphanumeric_field(campaign_with_model_prototype.name, "nombre de campaña")
    validate_positive_integer_field(campaign_with_model_prototype.printer_id, "ID del impresor")
    validate_positive_decimal_field(campaign_with_model_prototype.pledge_price, "precio de la reserva")
    validate_campaign_pledgers_interval(campaign_with_model_prototype.min_pledgers, campaign_with_model_prototype.max_pledgers)
    validate_tech_detail_prototype(campaign_with_model_prototype.tech_details)
    validate_future_date(campaign_with_model_prototype.end_date)


def validate_alphanumeric_field(field_value: str, field_name: str):
    if (field_value is None or
            field_value.isspace() or
            len(field_value) > 255 or
            (not all(c.isalnum() or c.isspace() for c in field_value))):
        raise InvalidParamException("El campo '{field_name}' es inválido".format(field_name=field_name))


def validate_url_field(field_value: str, field_name: str):
    if (field_value is None or
            field_value.isspace() or
            len(field_value) > 255):
        raise InvalidParamException("El campo '{field_name}' es inválido".format(field_name=field_name))


def validate_positive_integer_field(field_value: int, field_name: str):
    if (field_value is None or
            field_value <= 0):
        raise InvalidParamException("El campo '{field_name}' es inválido".format(field_name=field_name))


def validate_positive_decimal_field(field_value: float, field_name: str):
    if (field_value is None or
            field_value <= 0):
        raise InvalidParamException("El campo '{field_name}' es inválido".format(field_name=field_name))


def validate_time_interval(start_date: datetime.datetime, end_date: datetime.datetime):
    validate_future_date(start_date)
    validate_future_date(end_date)
    if start_date >= end_date:
        raise InvalidParamException("La fecha de inicio no puede ser igual o mayor a la fecha de fin")


def validate_future_date(date: datetime.datetime):
    if date is None or date <= datetime.datetime.now():
        raise InvalidParamException("The date must be a future date (bigger than now)")


def validate_campaign_pledgers_interval(min_pledgers: int, max_pledgers: int):
    if (min_pledgers is None or
            min_pledgers <= 0):
        raise InvalidParamException("El valor de la cantidad mínima de reservas es inválido")
    if max_pledgers is not None:
        if max_pledgers <= 0:
            raise InvalidParamException("El valor de la cantidad máxima de reservas es inválido")
        if min_pledgers > max_pledgers:
            raise InvalidParamException("La cantidad mínima de reservas no puede ser mayor a la cantidad máxima de reservas")


def validate_tech_detail_prototype(tech_details_prototype: TechDetailPrototype):
    validate_positive_integer_field(tech_details_prototype.weight, "peso del modelo 3D")
    validate_positive_integer_field(tech_details_prototype.width, "ancho del modelo 3D")
    validate_positive_integer_field(tech_details_prototype.length, "longitud del modelo 3D")
    validate_positive_integer_field(tech_details_prototype.depth, "altura del modelo 3D")


def validate_image_upload(file_dict: dict, image_name: str):
    if image_name not in file_dict:
        raise InvalidParamException("No se ha enviado ninguna imagen")

    if file_dict[image_name].mimetype not in VALID_IMAGE_MIMETYPES:
        raise InvalidParamException("Formato de imagen inválido. Solo se acepta el formato JPG")


def validate_image_file(image_file):
    if image_file.mimetype not in VALID_IMAGE_MIMETYPES:
        raise InvalidParamException("Formato de imagen inválido. Solo se acepta el formato JPG")


def validate_model_file_upload(file_dict: dict, image_name: str):
    if image_name not in file_dict:
        raise InvalidParamException("No se ha enviado ningun archivo de modelo 3D")

    image_file = file_dict[image_name]

    if not image_file.filename.lower().endswith(".stl"):
        raise InvalidParamException("Formato de archivo inválido. La extensión debe ser .stl")

    if image_file.mimetype not in VALID_MODEL_FILE_MIMETYPES:
        raise InvalidParamException("Formato de archivo inválido. Solo se acepta el formato STL")

