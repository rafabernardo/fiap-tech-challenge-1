from pydantic import BaseModel


class RegisterUserV1Request(BaseModel):
    name: str
    email: str
    cpf: str | None = None
