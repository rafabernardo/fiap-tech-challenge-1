from fastapi import APIRouter, Query, Response, status

from adapters.driven.repositories.order_repository import OrderMongoRepository
from adapters.driven.repositories.utils import get_pagination_info
from adapters.driver.entrypoints.v1.exceptions.commons import (
    ConflictErrorHTTPException,
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from adapters.driver.entrypoints.v1.models.commons import (
    DeleteDocumentV1Response,
)
from adapters.driver.entrypoints.v1.models.order import (
    ListOrderV1Response,
    OrderV1Response,
    PatchPaymentResultV1Request,
    RegisterOrderV1Request,
    RegisterOrderV1Response,
)
from core.application.exceptions.commons_exceptions import (
    DataConflictException,
    NoDocumentsFoundException,
)
from core.application.services.order_service import OrderService
from core.domain.models.order import Order

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/order")


@router.get("", response_model=ListOrderV1Response)
async def list_orders(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
) -> ListOrderV1Response:
    order_repository = OrderMongoRepository()
    order_service = OrderService(repository=order_repository)

    orders = order_service.list_orders(
        filter={}, page=page, page_size=page_size
    )
    total_orders = order_service.count_orders(filter={})

    pagination_info = get_pagination_info(
        total_results=total_orders, page=page, page_size=page_size
    )
    listed_orders = [OrderV1Response(**order.model_dump()) for order in orders]

    paginated_orders = ListOrderV1Response(
        **pagination_info.model_dump(), results=listed_orders
    )

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
    return paginated_orders


@router.get("/{id}", response_model=OrderV1Response)
async def get_user_by_id(id: str, response: Response) -> OrderV1Response:
    order_repository = OrderMongoRepository()
    order_service = OrderService(repository=order_repository)
    order = order_service.get_order_by_id(id)

    if order is None:
        raise NoDocumentsFoundHTTPException()

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
    return order


@router.post("", response_model=RegisterOrderV1Response)
async def register(
    create_order_request: RegisterOrderV1Request,
    response: Response,
):
    repository = OrderMongoRepository()
    service = OrderService(repository)
    order = Order(
        **create_order_request.model_dump(),
        status="pending",
        payment_status="pending",
    )
    try:
        created_order = service.register_order(order)
    except Exception:
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_order


@router.delete("/{id}", response_model=DeleteDocumentV1Response)
async def delete(id: str, response: Response) -> DeleteDocumentV1Response:
    repository = OrderMongoRepository()
    service = OrderService(repository)

    try:
        was_order_deleted = service.delete_order(id)
    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException(detail=exc.message)
    except Exception as exc:
        raise InternalServerErrorHTTPException()

    if not was_order_deleted:
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )


@router.patch("/payment-status/{order_id}")
async def set_payment_status(
    order_id: str,
    payment_result: PatchPaymentResultV1Request,
    response: Response,
):
    repository = OrderMongoRepository()
    service = OrderService(repository)

    try:
        service.set_payment_status(order_id, payment_result.result)
    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except DataConflictException:
        raise ConflictErrorHTTPException("Order payment can not be modified")
    except Exception:
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
