from datetime import datetime

from pydantic import BaseModel

from adapters.driver.entrypoints.v1.models.page import PageV1Response


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: int


class RegisterOrderV1Request(BaseModel):
    owner_id: str | None = None
    products: list[OrderItem]


class OrderV1Response(BaseModel):
    id: str | None = None
    owner_id: str | None = None

    order_number: int | None = None
    status: str
    products: list[OrderItem]
    payment_status: str

    created_at: datetime | None = None
    updated_at: datetime | None = None


class RegisterOrderV1Response(OrderV1Response): ...


class ListOrderV1Response(PageV1Response):
    results: list[OrderV1Response]


class PatchPaymentResultV1Request(BaseModel):
    result: bool
