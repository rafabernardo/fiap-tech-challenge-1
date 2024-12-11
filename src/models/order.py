from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator

from models.product import Product


class Status(Enum):
    pending = "pending"
    confirmed = "confirmed"
    received = "received"
    being_prepared = "being_prepared"
    ready = "ready"
    finished = "finished"
    # Only for orders that were not collected from client
    returned = "returned"

    canceled = "canceled"


class PaymentStatus(Enum):
    paid = "paid"
    pending = "pending"
    canceled = "canceled"


class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: int


class Order(BaseModel):
    id: int | None = None
    status: str  # Status
    products: list[OrderItem]
    created_at: datetime | None = None
    updated_at: datetime | None = None
    order_number: int | None = None
    owner_id: int | None = None
    payment_status: str  # PaymentStatus
    paid_at: datetime | None = None
    total_price: int

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        try:
            Status(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid status value: {v}")

    @field_validator("payment_status")
    @classmethod
    def validate_payment_status(cls, v: str):
        try:
            PaymentStatus(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid status value: {v}")


class OrderFilter(BaseModel):
    status: list[str] | None = None


class OrderOutput(Order):
    waiting_time: float | None = None
