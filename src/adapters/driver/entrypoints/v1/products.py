from fastapi import APIRouter, Query, Response, status

from adapters.driven.repositories.product_repository import (
    ProductMongoRepository,
)
from adapters.driven.repositories.utils import get_pagination_info
from adapters.driver.entrypoints.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
)
from adapters.driver.entrypoints.v1.models.product import (
    ListProductV1Response,
    ProductV1Request,
    ProductV1Response,
)
from core.application.services.product_service import ProductService
from core.domain.models.product import Category, Product

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/products")


@router.get("/", response_model=ListProductV1Response)
def list_products(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    category: Category = Query(None),
):
    try:
        repository = ProductMongoRepository()
        service = ProductService(repository)

        filter = {}
        if category:
            filter["category"] = category

        products = service.list_products(
            filter=filter,
            page=page,
            page_size=page_size,
        )
        total_products = service.count_products(filter=filter)

        pagination_info = get_pagination_info(
            total_results=total_products, page=page, page_size=page_size
        )

        listed_products = [
            ProductV1Response(**product.model_dump()) for product in products
        ]

        paginated_orders = ListProductV1Response(
            **pagination_info.model_dump(), results=listed_products
        )

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return paginated_orders
    except Exception:
        raise InternalServerErrorHTTPException()


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
    except Exception:
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
