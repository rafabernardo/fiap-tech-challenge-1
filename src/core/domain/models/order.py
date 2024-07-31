from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator

from core.domain.models.user import User


class Status(Enum):
    pending = "pending"
    confirmed = "confirmed"
    received = "received"
    being_prepared = "being_prepared"
    finished = "finished"
    returned = "returned"
    canceled = "canceled"


class PaymentStatus(Enum):
    paid = "paid"
    pending = "pending"
    canceled = "canceled"


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: int


class Order(BaseModel):
    id: str | None = None
    status: str  # Status
    products: list[OrderItem]
    created_at: datetime
    updated_at: datetime
    owner: User | None = None
    payment_status: str  # PaymentStatus

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        try:
            return Status(v)
        except ValueError:
            raise ValueError(f"Invalid status value: {v}")

    @field_validator("payment_status")
    @classmethod
    def validate_payment_status(cls, v: str):
        try:
            return PaymentStatus(v)
        except ValueError:
            raise ValueError(f"Invalid status value: {v}")
