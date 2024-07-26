from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from core.domain.models import User
from core.domain.models import Product

class OrderItem(BaseModel):
    order_item_id: int
    product: Product
    quantity: int
    price: int


class Order(BaseModel):
    order_id: int
    status: str
    products: list[OrderItem]
    created_at: datetime
    updated_at: datetime
    owner: Optional[User] = None
    payment_status: str
