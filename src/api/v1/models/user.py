from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RegisterUserV1Request(BaseModel):
    name: str
    email: str
    cpf: str | None = None


class UserV1Response(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="ignore")


class IdentifyUserV1Request(BaseModel):
    cpf: str
