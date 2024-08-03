from datetime import datetime

from pydantic import BaseModel


class RegisterUserV1Request(BaseModel):
    name: str
    email: str
    cpf: str | None = None


class RegisterUserV1Response(BaseModel):
    id: str
    name: str
    email: str
    cpf: str | None = None
    created_at: datetime
    updated_at: datetime
