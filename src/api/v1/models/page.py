from pydantic import BaseModel


class PageV1Response(BaseModel):
    total_results: int | None
    page: int | None
    page_size: int | None
    total_pages: int | None
    has_next: bool
    has_previous: bool
