from datetime import datetime

from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: int


class RegisterOrderV1Request(BaseModel):
    owner_id: str | None = None
    products: list[OrderItem]


class RegisterOrderV1Response(BaseModel):
    id: str | None = None
    owner_id: str | None = None

    order_number: int | None = None
    status: str
    products: list[OrderItem]
    payment_status: str

    created_at: datetime | None = None
    updated_at: datetime | None = None
