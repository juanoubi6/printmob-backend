import datetime

import pytest

from my_app.api.controllers.validators import validate_pagination_filters, validate_alphanumeric_field, \
    validate_url_field, validate_positive_integer_field, validate_positive_decimal_field, \
    validate_future_date, validate_campaign_pledgers_interval
from my_app.api.exceptions import InvalidParamException


def test_validate_pagination_filters_throws_exception_on_invalid_page():
    filter_with_invalid_page = {"page": "text", "page_size": "4"}

    with pytest.raises(InvalidParamException):
        validate_pagination_filters(filter_with_invalid_page)


def test_validate_pagination_filters_throws_exception_on_negative_page():
    filter_with_invalid_page = {"page": "-1", "page_size": "4"}

    with pytest.raises(InvalidParamException):
        validate_pagination_filters(filter_with_invalid_page)


def test_validate_pagination_filters_throws_exception_on_invalid_page_size():
    filter_with_invalid_page = {"page": "4", "page_size": "text"}

    with pytest.raises(InvalidParamException):
        validate_pagination_filters(filter_with_invalid_page)


def test_validate_pagination_filters_throws_exception_on_negative_page_size():
    filter_with_invalid_page = {"page": "4", "page_size": "-1"}

    with pytest.raises(InvalidParamException):
        validate_pagination_filters(filter_with_invalid_page)


def test_validate_pagination_works_with_valid_pagination_filters():
    filter_with_invalid_page = {"page": "4", "page_size": "5"}

    validate_pagination_filters(filter_with_invalid_page)


def test_validate_alphanumeric_field_works_with_valid_value():
    validate_alphanumeric_field("valid", "field")


def test_validate_alphanumeric_field_throws_exception_with_none_value():
    with pytest.raises(InvalidParamException):
        validate_alphanumeric_field(None, "field")


def test_validate_alphanumeric_field_throws_exception_with_all_spaces_value():
    with pytest.raises(InvalidParamException):
        validate_alphanumeric_field(" ", "field")


def test_validate_alphanumeric_field_throws_exception_with_large_value():
    with pytest.raises(InvalidParamException):
        validate_alphanumeric_field("a"*256, "field")


def test_validate_alphanumeric_field_throws_exception_with_not_alnum_value():
    with pytest.raises(InvalidParamException):
        validate_alphanumeric_field("$", "field")


def test_validate_url_field_works_with_valid_value():
    validate_url_field("valid", "field")


def test_validate_url_field_throws_exception_with_none_value():
    with pytest.raises(InvalidParamException):
        validate_url_field(None, "field")


def test_validate_url_field_throws_exception_with_all_spaces_value():
    with pytest.raises(InvalidParamException):
        validate_url_field(" ", "field")


def test_validate_url_field_throws_exception_with_large_value():
    with pytest.raises(InvalidParamException):
        validate_url_field("a"*256, "field")


def test_validate_integer_field_works_with_positive_value():
    validate_positive_integer_field(1, "field")


def test_validate_integer_field_throws_exception_with_none_value():
    with pytest.raises(InvalidParamException):
        validate_positive_integer_field(None, "field")


def test_validate_integer_field_throws_exception_with_zero_value():
    with pytest.raises(InvalidParamException):
        validate_positive_integer_field(0, "field")


def test_validate_integer_field_throws_exception_with_negative_value():
    with pytest.raises(InvalidParamException):
        validate_positive_integer_field(-1, "field")


def test_validate_decimal_field_works_with_positive_value():
    validate_positive_decimal_field(1.0, "field")


def test_validate_decimal_field_throws_exception_with_none_value():
    with pytest.raises(InvalidParamException):
        validate_positive_decimal_field(None, "field")


def test_validate_decimal_field_throws_exception_with_zero_value():
    with pytest.raises(InvalidParamException):
        validate_positive_decimal_field(0.0, "field")


def test_validate_decimal_field_throws_exception_with_negative_value():
    with pytest.raises(InvalidParamException):
        validate_positive_decimal_field(-1.0, "field")


def test_validate_end_date_works_with_valid_values():
    end_date = datetime.datetime.now() + datetime.timedelta(days=2)
    validate_future_date(end_date, "end_date")


def test_validate_end_date_throws_exception_with_none_end_date():
    with pytest.raises(InvalidParamException):
        validate_future_date(None, "end_date")


def test_validate_end_date_throws_exception_with_past_end_date():
    end_date = datetime.datetime.now() + datetime.timedelta(days=-2)
    with pytest.raises(InvalidParamException):
        validate_future_date(end_date, "end_date")


def test_validate_campaign_pledgers_interval_works_with_valid_values():
    validate_campaign_pledgers_interval(1, 2)


def test_validate_campaign_pledgers_interval_works_with_equals_values():
    validate_campaign_pledgers_interval(2, 2)


def test_validate_campaign_pledgers_interval_throws_exception_with_none_min_pledgers():
    with pytest.raises(InvalidParamException):
        validate_campaign_pledgers_interval(None, 2)


def test_validate_campaign_pledgers_interval_throws_exception_with_zero_min_pledgers():
    with pytest.raises(InvalidParamException):
        validate_campaign_pledgers_interval(0, 2)


def test_validate_campaign_pledgers_interval_throws_exception_with_negative_min_pledgers():
    with pytest.raises(InvalidParamException):
        validate_campaign_pledgers_interval(-1, 2)


def test_validate_campaign_pledgers_interval_throws_exception_with_zero_max_pledgers():
    with pytest.raises(InvalidParamException):
        validate_campaign_pledgers_interval(2, 0)


def test_validate_campaign_pledgers_interval_throws_exception_with_negative_max_pledgers():
    with pytest.raises(InvalidParamException):
        validate_campaign_pledgers_interval(2, -1)


def test_validate_campaign_pledgers_interval_throws_exception_with_invalid_pledgers_interval():
    with pytest.raises(InvalidParamException):
        validate_campaign_pledgers_interval(2, 1)
