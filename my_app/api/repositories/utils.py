from sqlalchemy import func

from my_app.api.repositories.models import CampaignModel

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


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
    page = int(filters.get("page", DEFAULT_PAGE))
    page_size = int(filters.get("page_size", DEFAULT_PAGE_SIZE))

    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE

    return query.limit(page_size).offset((page - 1) * page_size)


def apply_campaign_filters(query, filters: dict):
    """
    Applies filters to query

    Parameters
    ----------
    query: BaseQuery
        Query to paginate
    filters: dict[str,str]
        Dict with filters to apply.

    Returns
    ----------
    query: BaseQuery
        Query with limit and offset
    """
    # Status filter
    status = filters.get("status", None)
    if status is not None:
        query = query.filter(func.lower(CampaignModel.status) == status.lower())

    # Printer ID filter
    printer_id = filters.get("printer_id", None)
    if printer_id is not None:
        query = query.filter(CampaignModel.printer_id == printer_id)

    return query
