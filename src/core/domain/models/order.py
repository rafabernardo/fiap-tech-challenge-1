from datetime import datetime
from typing import Optional

from core.domain.models.product import Product
from core.domain.models.user import User
from pydantic import BaseModel


class OrderItem(BaseModel):
    id: int
    product: Product
    quantity: float
    price: float


class Order(BaseModel):
    id: int
    status: str
    products: list[OrderItem]
    created_at: datetime
    updated_at: datetime
    owner: Optional[User] = None
    payment_status: str
