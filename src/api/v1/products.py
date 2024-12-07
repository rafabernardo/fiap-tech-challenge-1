import traceback

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from api.v1.models.product import (
    ListProductV1Response,
    ProductPatchV1Request,
    ProductV1Request,
    ProductV1Response,
)
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
from models.product import Category, Product
from repositories.utils import clean_up_dict, get_pagination_info
from services.product_service import ProductService

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/products")


@router.get("/", response_model=ListProductV1Response)
@inject
def list_products(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    category: Category = Query(None),
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
):
    try:

        filter = {}
        if category:
            filter["category"] = category.value

        products = product_service.list_products(
            filter=filter,
            page=page,
            page_size=page_size,
        )
        total_products = product_service.count_products(filter=filter)

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
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()


@router.get("/{id}", response_model=ProductV1Response)
@inject
async def get_product_by_id(
    id: int,
    response: Response,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
):
    try:
        product = product_service.get_product_by_id(id)
    except Exception as e:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    if not product:
        raise NoDocumentsFoundHTTPException()
    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return product


@router.post("", response_model=ProductV1Response)
@inject
async def register(
    create_product_request: ProductV1Request,
    response: Response,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
):

    try:
        product = Product(**create_product_request.model_dump())
        product = product_service.register_product(product)
    except Exception as e:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return product


@router.delete("/{id}")
@inject
async def delete(
    id: int,
    response: Response,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
):

    try:
        was_product_deleted = product_service.delete_product(id)
        if not was_product_deleted:
            raise InternalServerErrorHTTPException()

    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )


@router.patch("/{id}", response_model=ProductV1Response)
@inject
async def update(
    id: int,
    product_request: ProductPatchV1Request,
    response: Response,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
):

    try:
        cleaned_product_request = clean_up_dict(product_request.model_dump())
        product = product_service.update_product(id, **cleaned_product_request)

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return product
    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()
