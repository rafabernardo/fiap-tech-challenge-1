import copy
from datetime import datetime

from adapters.driver.entrypoints.v1.models.page import PageV1Response


def replace_id_key(document: dict):
    data = copy.deepcopy(document)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
    return data


def prepare_document_to_db(
    document: dict, pop_id: bool = True, skip_created_at: bool = False
):
    data = copy.deepcopy(document)
    now = datetime.now()

    if pop_id:
        data.pop("id", None)
    data["updated_at"] = now
    if data.get("created_at") is None and not skip_created_at:
        data["created_at"] = now
    return data


def get_pagination_info(
    total_results=int, page=int, page_size=int
) -> PageV1Response:
    total_pages = (total_results + page_size - 1) // page_size
    has_next = page < total_pages
    has_previous = page > 1

    pagination_info = PageV1Response(
        total_results=total_results,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=has_next,
        has_previous=has_previous,
    )
    return pagination_info
