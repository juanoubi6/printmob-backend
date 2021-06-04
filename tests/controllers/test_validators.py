import pytest

from my_app.api.controllers.validators import validate_pagination_filters
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
