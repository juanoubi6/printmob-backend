from my_app.api.repositories.models import CampaignModel, PledgeModel, OrderModel

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
        Query with filters
    """
    # Status filter
    status = filters.get("status", None)
    if status is not None:
        statuses = status.split(",")
        query = query.filter(CampaignModel.status.in_(statuses))

    # Printer ID filter
    printer_id = filters.get("printer_id", None)
    if printer_id is not None:
        query = query.filter(CampaignModel.printer_id == printer_id)

    return query


def apply_campaign_order_filters(query, filters: dict):
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
        Query with filters
    """
    # Status filter
    status = filters.get("status", None)
    if status is not None:
        statuses = status.split(",")
        query = query.filter(OrderModel.status.in_(statuses))

    return query


def apply_pledge_filters(query, filters: dict):
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
        Query with filters
    """
    # Buyer filter
    buyer_id = filters.get("buyer_id", None)
    if buyer_id is not None:
        query = query.filter(PledgeModel.buyer_id == int(buyer_id))

    # Campaign filter
    campaign_id = filters.get("campaign_id", None)
    if campaign_id is not None:
        query = query.filter(PledgeModel.campaign_id == int(campaign_id))

    return query
