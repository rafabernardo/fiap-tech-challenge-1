from datetime import datetime

from pydantic import BaseModel, field_validator

from api.v1.models.page import PageV1Response
from models.product import Category


class ProductV1Request(BaseModel):
    name: str
    category: str
    price: int
    description: str
    image: str

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str):
        try:
            Category(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid category value: {v}")


class ProductPatchV1Request(ProductV1Request):
    name: str | None = None
    category: str | None = None
    price: int | None = None
    description: str | None = None
    image: str | None = None


class ProductV1Response(ProductV1Request):
    id: int
    created_at: datetime
    updated_at: datetime


class ListProductV1Response(PageV1Response):
    results: list[ProductV1Response]
