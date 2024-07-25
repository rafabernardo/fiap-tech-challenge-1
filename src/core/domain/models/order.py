from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from core.domain.models import User
from core.domain.models import Product

class Order(BaseModel):
    order_id: int
    status: str
    products: list[Product]
    created_at: datetime
    updated_at: datetime
    owner: Optional[User] = None
    payment_status: str
