from fastapi import APIRouter, Query, Response, status

from adapters.driven.repositories.order_repository import OrderMongoRepository
from adapters.driven.repositories.product_repository import (
    ProductMongoRepository,
)
from adapters.driven.repositories.queue_repository import QueueMongoRepository
from adapters.driven.repositories.user_repository import UserMongoRepository
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
from adapters.driver.entrypoints.v1.models.queue import (
    ListQueueV1Response,
    QueueItemV1Response,
)
from core.application.exceptions.commons_exceptions import (
    DataConflictException,
    NoDocumentsFoundException,
)
from core.application.services.order_service import OrderService
from core.application.services.product_service import ProductService
from core.application.services.queue_service import QueueService
from core.application.services.user_service import UserService
from core.domain.models.order import OrderFilter, Status
from core.domain.models.queue import QueueItem

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/order")


@router.get("/queue", response_model=ListQueueV1Response)
async def list_queue_items(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
) -> ListQueueV1Response:
    queue_repository = QueueMongoRepository()
    queue_service = QueueService(queue_repository)

    queue_items = queue_service.list_queue_items(
        filter={}, page=page, page_size=page_size
    )
    total_queue_items = queue_service.count_queue_items(filter={})

    pagination_info = get_pagination_info(
        total_results=total_queue_items, page=page, page_size=page_size
    )
    listed_queue_items = [
        QueueItemV1Response(**queue_item.model_dump())
        for queue_item in queue_items
    ]

    paginated_queue_items = ListQueueV1Response(
        **pagination_info.model_dump(), results=listed_queue_items
    )

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
    return paginated_queue_items


@router.get("", response_model=ListOrderV1Response)
async def list_orders(
    response: Response,
    order_status: list[Status] = Query(None),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
) -> ListOrderV1Response:
    repository = OrderMongoRepository()
    service = OrderService(repository)

    orders_filter = OrderFilter(status=order_status)

    orders = service.list_orders(
        order_filter=orders_filter, page=page, page_size=page_size
    )
    total_orders = service.count_orders(order_filter=orders_filter)

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
async def get_order_by_id(id: str, response: Response) -> OrderV1Response:
    repository = OrderMongoRepository()
    service = OrderService(repository)
    order = service.get_order_by_id(id)

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
    user_repository = UserMongoRepository()
    product_repository = ProductMongoRepository()
    order_service = OrderService(repository)
    user_service = UserService(user_repository)
    product_service = ProductService(product_repository)

    try:
        if create_order_request.owner_id:
            user = user_service.get_user_by_id(create_order_request.owner_id)
            if user is None:
                message = (
                    f"No User found with id '{create_order_request.owner_id}'"
                )
                raise NoDocumentsFoundException(message)

        for product in create_order_request.products:
            found_product = product_service.get_product_by_id(
                product.product_id
            )
            if found_product is None:
                message = f"No Product found with id '{product.product_id}'"
                raise NoDocumentsFoundException(message)

        order = order_service.prepare_new_order(
            create_order_request.model_dump()
        )
        created_order = order_service.register_order(order)
    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException(exc.message)
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
    except Exception:
        raise InternalServerErrorHTTPException()

    if not was_order_deleted:
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )


@router.patch("/fake-checkout/{order_id}")
async def set_payment_status(
    order_id: str,
    payment_result: PatchPaymentResultV1Request,
    response: Response,
):
    repository = OrderMongoRepository()
    service = OrderService(repository)
    queue_repository = QueueMongoRepository()
    queue_service = QueueService(queue_repository)

    try:
        service.set_payment_status(order_id, payment_result.result)
        queue_service.register_queue_item(QueueItem(id=order_id))
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
