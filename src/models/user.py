from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    email: str
    cpf: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
