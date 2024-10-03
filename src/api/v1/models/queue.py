from datetime import datetime

from pydantic import BaseModel

from api.v1.models.page import PageV1Response


class QueueItemV1Response(BaseModel):
    id: str
    created_at: datetime
    order_id: str


class ListQueueV1Response(PageV1Response):
    results: list[QueueItemV1Response]
