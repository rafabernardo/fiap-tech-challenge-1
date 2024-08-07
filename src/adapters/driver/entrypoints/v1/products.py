from typing import Optional

from fastapi import APIRouter, Response, status

from adapters.driven.repositories.product_repository import (
    ProductMongoRepository,
)
from adapters.driver.entrypoints.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
)
from adapters.driver.entrypoints.v1.models.product import (
    ProductV1Request,
    ProductV1Response,
)
from core.application.services.product_service import ProductService
from core.domain.models.product import Product

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/products")


@router.get("/")
def list_products(category: Optional[str] = None):
    return {"msg": category}


@router.get("/{id}")
async def get_product_by_id(id: int):
    return {"msg": id}


@router.post("", response_model=ProductV1Response)
async def register(
    create_product_request: ProductV1Request,
    response: Response,
):
    repository = ProductMongoRepository()
    service = ProductService(repository)

    try:
        product = Product(**create_product_request.model_dump())
        product = service.register_product(product)
    except Exception as e:
        print(e)
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return product


@router.delete("/delete/{id}")
async def delete(id: int):
    return {"msg": id}


@router.patch("/{id}")
async def update(id: int):
    return {"msg": id}
