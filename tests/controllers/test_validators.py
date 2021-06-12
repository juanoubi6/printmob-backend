import datetime
import unittest

import pytest

from my_app.api.controllers.validators import validate_pagination_filters, validate_alphanumeric_field, \
    validate_url_field, validate_positive_integer_field, validate_positive_decimal_field, \
    validate_campaign_time_interval, validate_campaign_pledgers_interval
from my_app.api.exceptions import InvalidParamException


class TestValidators(unittest.TestCase):

    def test_validate_pagination_filters_throws_exception_on_invalid_page(self):
        filter_with_invalid_page = {"page": "text", "page_size": "4"}

        with pytest.raises(InvalidParamException):
            validate_pagination_filters(filter_with_invalid_page)

    def test_validate_pagination_filters_throws_exception_on_negative_page(self):
        filter_with_invalid_page = {"page": "-1", "page_size": "4"}

        with pytest.raises(InvalidParamException):
            validate_pagination_filters(filter_with_invalid_page)

    def test_validate_pagination_filters_throws_exception_on_invalid_page_size(self):
        filter_with_invalid_page = {"page": "4", "page_size": "text"}

        with pytest.raises(InvalidParamException):
            validate_pagination_filters(filter_with_invalid_page)

    def test_validate_pagination_filters_throws_exception_on_negative_page_size(self):
        filter_with_invalid_page = {"page": "4", "page_size": "-1"}

        with pytest.raises(InvalidParamException):
            validate_pagination_filters(filter_with_invalid_page)

    def test_validate_pagination_works_with_valid_pagination_filters(self):
        filter_with_invalid_page = {"page": "4", "page_size": "5"}

        validate_pagination_filters(filter_with_invalid_page)

    def test_validate_alphanumeric_field_works_with_valid_value(self):
        validate_alphanumeric_field("valid", "field")

    def test_validate_alphanumeric_field_throws_exception_with_none_value(self):
        with pytest.raises(InvalidParamException):
            validate_alphanumeric_field(None, "field")

    def test_validate_alphanumeric_field_throws_exception_with_all_spaces_value(self):
        with pytest.raises(InvalidParamException):
            validate_alphanumeric_field(" ", "field")

    def test_validate_alphanumeric_field_throws_exception_with_large_value(self):
        with pytest.raises(InvalidParamException):
            validate_alphanumeric_field("a" * 256, "field")

    def test_validate_alphanumeric_field_throws_exception_with_not_alnum_value(self):
        with pytest.raises(InvalidParamException):
            validate_alphanumeric_field("$", "field")

    def test_validate_url_field_works_with_valid_value(self):
        validate_url_field("valid", "field")

    def test_validate_url_field_throws_exception_with_none_value(self):
        with pytest.raises(InvalidParamException):
            validate_url_field(None, "field")

    def test_validate_url_field_throws_exception_with_all_spaces_value(self):
        with pytest.raises(InvalidParamException):
            validate_url_field(" ", "field")

    def test_validate_url_field_throws_exception_with_large_value(self):
        with pytest.raises(InvalidParamException):
            validate_url_field("a" * 256, "field")

    def test_validate_integer_field_works_with_positive_value(self):
        validate_positive_integer_field(1, "field")

    def test_validate_integer_field_throws_exception_with_none_value(self):
        with pytest.raises(InvalidParamException):
            validate_positive_integer_field(None, "field")

    def test_validate_integer_field_throws_exception_with_zero_value(self):
        with pytest.raises(InvalidParamException):
            validate_positive_integer_field(0, "field")

    def test_validate_integer_field_throws_exception_with_negative_value(self):
        with pytest.raises(InvalidParamException):
            validate_positive_integer_field(-1, "field")

    def test_validate_decimal_field_works_with_positive_value(self):
        validate_positive_decimal_field(1.0, "field")

    def test_validate_decimal_field_throws_exception_with_none_value(self):
        with pytest.raises(InvalidParamException):
            validate_positive_decimal_field(None, "field")

    def test_validate_decimal_field_throws_exception_with_zero_value(self):
        with pytest.raises(InvalidParamException):
            validate_positive_decimal_field(0.0, "field")

    def test_validate_decimal_field_throws_exception_with_negative_value(self):
        with pytest.raises(InvalidParamException):
            validate_positive_decimal_field(-1.0, "field")

    def test_validate_campaign_interval_works_with_valid_values(self):
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() + datetime.timedelta(days=2)
        validate_campaign_time_interval(start_date, end_date)

    def test_validate_campaign_interval_throws_exception_with_none_start_date(self):
        end_date = datetime.datetime.now() + datetime.timedelta(days=2)
        with pytest.raises(InvalidParamException):
            validate_campaign_time_interval(None, end_date)

    def test_validate_campaign_interval_throws_exception_with_past_start_date(self):
        start_date = datetime.datetime.now() + datetime.timedelta(days=-1)
        end_date = datetime.datetime.now() + datetime.timedelta(days=2)
        with pytest.raises(InvalidParamException):
            validate_campaign_time_interval(start_date, end_date)

    def test_validate_campaign_interval_throws_exception_with_none_end_date(self):
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        with pytest.raises(InvalidParamException):
            validate_campaign_time_interval(start_date, None)

    def test_validate_campaign_interval_throws_exception_with_past_end_date(self):
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() + datetime.timedelta(days=-2)
        with pytest.raises(InvalidParamException):
            validate_campaign_time_interval(start_date, end_date)

    def test_validate_campaign_interval_throws_exception_with_invalid_interval(self):
        start_date = datetime.datetime.now() + datetime.timedelta(days=2)
        end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        with pytest.raises(InvalidParamException):
            validate_campaign_time_interval(start_date, end_date)

    def test_validate_campaign_pledgers_interval_works_with_valid_values(self):
        validate_campaign_pledgers_interval(1, 2)

    def test_validate_campaign_pledgers_interval_works_with_equals_values(self):
        validate_campaign_pledgers_interval(2, 2)

    def test_validate_campaign_pledgers_interval_throws_exception_with_none_min_pledgers(self):
        with pytest.raises(InvalidParamException):
            validate_campaign_pledgers_interval(None, 2)

    def test_validate_campaign_pledgers_interval_throws_exception_with_zero_min_pledgers(self):
        with pytest.raises(InvalidParamException):
            validate_campaign_pledgers_interval(0, 2)

    def test_validate_campaign_pledgers_interval_throws_exception_with_negative_min_pledgers(self):
        with pytest.raises(InvalidParamException):
            validate_campaign_pledgers_interval(-1, 2)

    def test_validate_campaign_pledgers_interval_throws_exception_with_zero_max_pledgers(self):
        with pytest.raises(InvalidParamException):
            validate_campaign_pledgers_interval(2, 0)

    def test_validate_campaign_pledgers_interval_throws_exception_with_negative_max_pledgers(self):
        with pytest.raises(InvalidParamException):
            validate_campaign_pledgers_interval(2, -1)

    def test_validate_campaign_pledgers_interval_throws_exception_with_invalid_pledgers_interval(self):
        with pytest.raises(InvalidParamException):
            validate_campaign_pledgers_interval(2, 1)
