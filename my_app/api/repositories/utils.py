DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


def paginate(query, filters: dict):
    """
    Applies pagination from filters to the given query

    Parameterscampaign_repository.get_campaign_detail(1)
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
    page = int(filters.get("page", DEFAULT_PAGE))
    page_size = int(filters.get("page_size", DEFAULT_PAGE_SIZE))

    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE

    return query.limit(page_size).offset((page - 1) * page_size)
