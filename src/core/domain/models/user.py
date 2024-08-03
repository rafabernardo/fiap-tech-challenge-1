from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    name: str
    email: str
    cpf: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
