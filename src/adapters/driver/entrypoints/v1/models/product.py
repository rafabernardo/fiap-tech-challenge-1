from datetime import datetime

from pydantic import BaseModel, field_validator

from core.domain.models.product import Category


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


class ProductV1Response(ProductV1Request):
    id: str
    created_at: datetime
    updated_at: datetime
