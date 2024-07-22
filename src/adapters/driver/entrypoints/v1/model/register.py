from pydantic import BaseModel

class Register(BaseModel):
    id: int
    name: str | None = None
    email: str | None = None
    cpf: str | None = None
