from unittest.mock import MagicMock

from my_app.api.repositories.utils import paginate, DEFAULT_PAGE_SIZE, DEFAULT_PAGE


def test_paginate_applies_default_values_when_pagination_filters_are_missing():
    query_mock = MagicMock()
    empty_filters = {}

    paginate(query_mock, empty_filters)

    query_mock.limit.assert_called_once_with(DEFAULT_PAGE_SIZE)
    query_mock.limit.return_value.offset.assert_called_once_with((DEFAULT_PAGE - 1) * DEFAULT_PAGE_SIZE)


def test_paginate_applies_given_filters_when_pagination_filters_are_present():
    query_mock = MagicMock()
    filters = {"page": 10, "page_size": 20}

    paginate(query_mock, filters)

    query_mock.limit.assert_called_once_with(20)
    query_mock.limit.return_value.offset.assert_called_once_with((10 - 1) * 20)
