from pydantic import BaseModel


class CreateUserV1Request(BaseModel):
    name: str
    email: str
    cpf: str | None = None
