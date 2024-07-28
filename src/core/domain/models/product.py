from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: int
    description: str
    image: str
