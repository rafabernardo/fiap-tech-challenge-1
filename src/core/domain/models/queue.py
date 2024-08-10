from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QueueItem(BaseModel):
    id: str
    created_at: datetime | None = None

    model_config = ConfigDict(extra="ignore")
