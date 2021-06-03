DEFAULT_PAGE = "1"
DEFAULT_PAGE_SIZE = "10"


def paginate(query, filters: dict):
    """
    Applies pagination from filters to the given query

    Parameters
    ----------
    query: BaseQuery
        Query to paginate
    filters: dict[str,str]
        Dict with pagination filters to apply.

    Returns
    ----------
    query: BaseQuery
        Query with limit and offset
    """
    return query.limit(
        int(filters.get("page_size", DEFAULT_PAGE_SIZE))
    ).offset(
        (int(filters.get("page", DEFAULT_PAGE)) - 1) * int(filters.get("page_size", DEFAULT_PAGE_SIZE))
    )
