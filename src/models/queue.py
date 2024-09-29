from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QueueItem(BaseModel):
    id: str | None = None
    created_at: datetime | None = None
    order_id: str

    model_config = ConfigDict(extra="ignore")
