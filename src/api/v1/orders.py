import traceback

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status

from api.v1.exceptions.commons import (
    ConflictErrorHTTPException,
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from api.v1.models.order import (
    ListOrderV1Response,
    OrderItemV1Response,
    OrderPatchV1Request,
    OrderV1Response,
    PatchPaymentResultV1Request,
    PaymentStatusV1Response,
    RegisterOrderV1Request,
    RegisterOrderV1Response,
)
from api.v1.models.queue import ListQueueV1Response, QueueItemV1Response
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import (
    DataConflictException,
    NoDocumentsFoundException,
)
from models.order import OrderFilter, Status
from models.queue import QueueItem
from repositories.utils import clean_up_dict, get_pagination_info
from services.order_service import OrderService
from services.product_service import ProductService
from services.queue_service import QueueService
from services.user_service import UserService

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/order")


@router.get("/queue", response_model=ListQueueV1Response)
@inject
async def list_queue_items(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    queue_service: QueueService = Depends(Provide[Container.queue_service]),
) -> ListQueueV1Response:

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
@inject
async def list_orders(
    response: Response,
    order_status: list[Status] = Query(None),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    order_service: OrderService = Depends(Provide[Container.order_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> ListOrderV1Response:

    orders_filter = OrderFilter(status=order_status)

    orders = order_service.list_orders(
        order_filter=orders_filter, page=page, page_size=page_size
    )
    total_orders = order_service.count_orders(order_filter=orders_filter)

    pagination_info = get_pagination_info(
        total_results=total_orders, page=page, page_size=page_size
    )
    listed_orders = []
    for order in orders:
        owner_data = (
            user_service.get_user_by_id(order.owner_id).model_dump()
            if order.owner_id
            else None
        )
        order_response = OrderV1Response(
            **order.model_dump(), owner=owner_data
        )
        listed_orders.append(order_response)

    paginated_orders = ListOrderV1Response(
        **pagination_info.model_dump(), results=listed_orders
    )

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
    return paginated_orders


@router.get("/{id}", response_model=OrderV1Response)
@inject
async def get_order_by_id(
    id: str,
    response: Response,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> OrderV1Response:

    order = order_service.get_order_by_id(id)
    if order is None:
        raise NoDocumentsFoundHTTPException()

    owner_data = (
        user_service.get_user_by_id(order.owner_id).model_dump()
        if order.owner_id
        else None
    )
    order_response = OrderV1Response(**order.model_dump(), owner=owner_data)

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
    return order_response


@router.post("", response_model=RegisterOrderV1Response)
@inject
async def register(
    create_order_request: RegisterOrderV1Request,
    response: Response,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
):
    try:
        if create_order_request.owner_id:
            user = user_service.get_user_by_id(create_order_request.owner_id)
            if user is None:
                message = (
                    f"No User found with id '{create_order_request.owner_id}'"
                )
                raise NoDocumentsFoundException(message)
        products_data = []
        for product in create_order_request.products:
            found_product = product_service.get_product_by_id(
                product.product_id
            )
            if found_product is None:
                message = f"No Product found with id '{product.product_id}'"
                raise NoDocumentsFoundException(message)
            price = product.quantity * found_product.price
            products_data.append(
                OrderItemV1Response(
                    product=found_product.model_dump(),
                    quantity=product.quantity,
                    price=price,
                ).model_dump()
            )

        order = order_service.prepare_new_order(
            create_order_request.model_dump(), products_data
        )

        created_order = order_service.register_order(order)

    except NoDocumentsFoundException as exc:
        print(traceback.format_exc())
        raise NoDocumentsFoundHTTPException(exc.message)
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_order


@router.delete("/{id}")
@inject
async def delete(
    id: str,
    response: Response,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    queue_service: QueueService = Depends(Provide[Container.queue_service]),
):

    try:
        queue_item = queue_service.get_queue_item_by_order_id(id)
        if queue_item is not None:
            queue_service.delete_queue_item(queue_item.id)
        was_order_deleted = order_service.delete_order(id)

        if was_order_deleted:
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        raise InternalServerErrorHTTPException()

    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException(detail=exc.message)
    except Exception:
        raise InternalServerErrorHTTPException()


@router.patch("/{id}", response_model=OrderV1Response)
@inject
async def update(
    id: str,
    order_request: OrderPatchV1Request,
    response: Response,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
) -> OrderV1Response:
    try:
        old_order = order_service.get_order_by_id(id)
        if old_order is None:
            raise NoDocumentsFoundException()
        cleaned_order_request = clean_up_dict(order_request.model_dump())
        new_order_items_data = cleaned_order_request.get("products")
        old_order_data = old_order.model_dump()
        old_order_items_data = old_order_data.get("products")
        if new_order_items_data:
            new_order_items_details = order_service.get_order_items_details(
                new_order_items_data, product_service
            )
            if new_order_items_details == old_order_items_data:
                cleaned_order_request.pop("products", None)
            else:
                prepared_order = order_service.prepare_new_order(
                    old_order_data, new_order_items_details
                )
                cleaned_order_request.update(
                    {
                        "products": new_order_items_details,
                        "total_price": prepared_order.total_price,
                    }
                )

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )
        if not cleaned_order_request:
            return old_order

        order = order_service.update_order(id, **cleaned_order_request)
        updated_order = OrderV1Response(**order.model_dump())
        return updated_order
    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except Exception:
        raise InternalServerErrorHTTPException()


@router.patch("/fake-checkout/{order_id}")
@inject
async def set_payment_status(
    order_id: str,
    payment_result: PatchPaymentResultV1Request,
    response: Response,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    queue_service: QueueService = Depends(Provide[Container.queue_service]),
):

    try:
        order_service.set_payment_status(order_id, payment_result.result)
        if payment_result.result is True:
            queue_item = QueueItem(order_id=order_id)
            queue_service.register_queue_item(queue_item)
    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except DataConflictException:
        raise ConflictErrorHTTPException("Order payment can not be modified")

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )


@router.get(
    "/get_payment_status/{order_id}", response_model=PaymentStatusV1Response
)
@inject
async def get_payment_status(
    order_id: str,
    response: Response,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    try:
        payment_status = order_service.get_payment_status(order_id)
        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        payment_status_response = {"payment_status": payment_status.value}

        return payment_status_response
    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except Exception:
        raise InternalServerErrorHTTPException()


@router.get("/display-orders/", response_model=ListOrderV1Response)
@inject
async def list_orders(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    order_service: OrderService = Depends(Provide[Container.order_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> ListOrderV1Response:

    orders = order_service.list_orders_to_display(
        page=page, page_size=page_size
    )
    order_filter = OrderFilter(
        status=[
            Status.ready.value,
            Status.received.value,
            Status.being_prepared.value,
        ]
    )
    total_orders = order_service.count_orders(order_filter=order_filter)

    pagination_info = get_pagination_info(
        total_results=total_orders, page=page, page_size=page_size
    )
    listed_orders = []
    for order in orders:
        owner_data = (
            user_service.get_user_by_id(order.owner_id).model_dump()
            if order.owner_id
            else None
        )
        order_response = OrderV1Response(
            **order.model_dump(), owner=owner_data
        )
        listed_orders.append(order_response)

    paginated_orders = ListOrderV1Response(
        **pagination_info.model_dump(), results=listed_orders
    )

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )
    return paginated_orders
