import datetime

from my_app.api.domain.campaign import CampaignPrototype
from my_app.api.domain.tech_detail import TechDetailPrototype
from my_app.api.exceptions import InvalidParamException

PAGE_FILTER_NAME = "page"
PAGE_SIZE_FILTER_NAME = "page_size"


def validate_pagination_filters(filters: dict):
    if PAGE_FILTER_NAME in filters:
        page_filter = filters[PAGE_FILTER_NAME]
        if (not page_filter.isnumeric()) or (int(page_filter) < 1):
            raise InvalidParamException("The query param 'page' should be numeric")

    if PAGE_SIZE_FILTER_NAME in filters:
        page_size_filter = filters[PAGE_SIZE_FILTER_NAME]
        if (not page_size_filter.isnumeric()) or (int(page_size_filter) < 1):
            raise InvalidParamException("The query param 'page_size' should be numeric")


def validate_campaign_prototype(campaign_prototype: CampaignPrototype):
    validate_alphanumeric_field(campaign_prototype.name, "name of the campaign")
    validate_alphanumeric_field(campaign_prototype.description, "description of the campaign")
    for image_url in campaign_prototype.campaign_model_image_urls:
        validate_url_field(image_url, "url of the campaign image")
    validate_positive_integer_field(campaign_prototype.printer_id, "id of the campaign printer")
    validate_positive_decimal_field(campaign_prototype.pledge_price, "price of the campaign pledge")
    validate_campaign_time_interval(campaign_prototype.start_date, campaign_prototype.end_date)
    validate_campaign_pledgers_interval(campaign_prototype.min_pledgers, campaign_prototype.max_pledgers)
    validate_tech_detail_prototype(campaign_prototype.tech_details)


def validate_alphanumeric_field(field_value: str, field_name: str):
    if (field_value is None or
            field_value.isspace() or
            len(field_value) > 255 or
            (not all(c.isalnum() or c.isspace() for c in field_value))):
        raise InvalidParamException("The {field_name} is invalid".format(field_name=field_name))


def validate_url_field(field_value: str, field_name: str):
    if (field_value is None or
            field_value.isspace() or
            len(field_value) > 255):
        raise InvalidParamException("The {field_name} is invalid".format(field_name=field_name))


def validate_positive_integer_field(field_value: int, field_name: str):
    if (field_value is None or
            field_value <= 0):
        raise InvalidParamException("The {field_name} is invalid".format(field_name=field_name))


def validate_positive_decimal_field(field_value: float, field_name: str):
    if (field_value is None or
            field_value <= 0):
        raise InvalidParamException("The {field_name} is invalid".format(field_name=field_name))


def validate_campaign_time_interval(start_date: datetime.datetime, end_date: datetime.datetime):
    now = datetime.datetime.now()
    if (start_date is None or
            start_date < now):
        raise InvalidParamException("The start date of the campaign is invalid")
    if (end_date is None or
            end_date < now):
        raise InvalidParamException("The end date of the campaign is invalid")
    if start_date >= end_date:
        raise InvalidParamException("The campaign time interval is invalid")


def validate_campaign_pledgers_interval(min_pledgers: int, max_pledgers: int):
    if (min_pledgers is None or
            min_pledgers <= 0):
        raise InvalidParamException("The minimum value of campaign pledgers is invalid")
    if max_pledgers <= 0:
        raise InvalidParamException("The maximum value of campaign pledgers is invalid")
    if min_pledgers > max_pledgers:
        raise InvalidParamException("The campaign pledges interval is invalid")


def validate_tech_detail_prototype(tech_details_prototype: TechDetailPrototype):
    validate_alphanumeric_field(tech_details_prototype.material, "material of the 3D model")
    validate_positive_integer_field(tech_details_prototype.weight, "weight of the 3D model")
    validate_positive_integer_field(tech_details_prototype.width, "weight of the 3D model")
    validate_positive_integer_field(tech_details_prototype.length, "weight of the 3D model")
    validate_positive_integer_field(tech_details_prototype.depth, "weight of the 3D model")
