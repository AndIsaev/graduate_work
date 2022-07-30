import math


def get_by_pagination(
    name: str, db_objects, total: int, page: int = 1, page_size: int = 20
) -> dict:
    """
    This method will try to paginate objects by page number
    :param name: name of model
    :param db_objects: object query
    :param total: total query count
    :param page: selected page number
    :param page_size: page size
    :return: dict containing: (
        list of invitations,
        selected page number,
        page size,
        previous page number,
        next page number,
        total available pages,
        total objects number
    )
    """
    next_page, previous_page = None, None
    if page > 1:
        previous_page = page - 1
    previous_items = (page - 1) * page_size
    if previous_items + len(db_objects) < total:
        next_page = page + 1
    pages: int = int(math.ceil(total / float(page_size)))
    return {
        f"{name}": db_objects,
        "page": page,
        "page_size": page_size,
        "previous_page": previous_page,
        "next_page": next_page,
        "available_pages": pages,
        "total": total,
    }
