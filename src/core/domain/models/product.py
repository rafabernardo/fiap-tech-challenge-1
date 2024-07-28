from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str
    image: str
