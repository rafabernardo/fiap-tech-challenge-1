from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: int
    description: str
    image: str