from my_app.api.exceptions import InvalidParamException

PAGE_FILTER_NAME = "page"
PAGE_SIZE_FILTER_NAME = "page_size"


def validate_pagination_filters(filters: dict):
    if (PAGE_FILTER_NAME in filters) and (not filters[PAGE_FILTER_NAME].isnumeric()):
        raise InvalidParamException("The query param 'page' should be numeric")

    if (PAGE_SIZE_FILTER_NAME in filters) and (not filters[PAGE_SIZE_FILTER_NAME].isnumeric()):
        raise InvalidParamException("The query param 'page_size' should be numeric")
