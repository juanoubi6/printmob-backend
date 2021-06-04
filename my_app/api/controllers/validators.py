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
