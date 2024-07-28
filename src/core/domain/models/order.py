from datetime import datetime
from enum import Enum
from typing import Optional

from core.domain.models.product import Product
from core.domain.models.user import User
from pydantic import BaseModel


class Status(Enum, str):
    pending = "pending"
    confirmed = "confirmed"
    received = "received"
    being_prepared = "being_prepared"
    finished = "finished"
    returned = "returned"
    canceled = "canceled"


class PaymentStatus(Enum, str):
    paid = "paid"
    pending = "pending"
    canceled = "canceled"


class OrderItem(BaseModel):
    id: int
    product: Product
    quantity: float
    price: float


class Order(BaseModel):
    id: int
    status: Status
    products: list[OrderItem]
    created_at: datetime
    updated_at: datetime
    owner: Optional[User] = None
    payment_status: PaymentStatus
