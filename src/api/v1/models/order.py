from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from api.v1.models.page import PageV1Response
from api.v1.models.product import ProductV1Response


class OrderItemV1Request(BaseModel):
    product_id: str
    quantity: int


class RegisterOrderV1Request(BaseModel):
    owner_id: str | None = None
    products: list[OrderItemV1Request]


class OrderItemV1Response(BaseModel):
    product: ProductV1Response
    quantity: int
    price: int


class OrderV1Response(BaseModel):
    id: int = None
    owner_id: int

    order_number: int | None = None
    status: str
    products: list[OrderItemV1Response] = Field(..., min_length=1)
    payment_status: str
    total_price: int

    created_at: datetime | None = None
    updated_at: datetime | None = None
    waiting_time: float | None = None

    model_config = ConfigDict(extra="ignore")


class RegisterOrderV1Response(OrderV1Response): ...


class ListOrderV1Response(PageV1Response):
    results: list[OrderV1Response]


class PatchPaymentResultV1Request(BaseModel):
    result: bool


class OrderPatchV1Request(BaseModel):
    products: list[OrderItemV1Request] | None = Field(None, min_length=1)
    status: str | None = None
    payment_status: str | None = None


class PaymentStatusV1Response(BaseModel):
    payment_status: str | None = None
