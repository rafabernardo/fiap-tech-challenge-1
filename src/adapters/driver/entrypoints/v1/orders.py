from fastapi import APIRouter, HTTPException, Query, Response, status

from adapters.driven.repositories.order_repository import OrderMongoRepository
from adapters.driven.repositories.utils import get_pagination_info
from adapters.driver.entrypoints.v1.models.order import (
    ListOrderV1Response,
    OrderV1Response,
    RegisterOrderV1Request,
    RegisterOrderV1Response,
)
from core.application.services.order_service import OrderService
from core.domain.models.order import Order

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/order")


@router.get("", response_model=ListOrderV1Response)
async def list_users(
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
    return paginated_orders


@router.get("/{id}")
async def get_user_by_id(id: str):
    return {"msg": id}


@router.post("/register", response_model=RegisterOrderV1Response)
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_order


@router.delete("/delete/{id}")
async def delete(id: str):
    return {"msg": id}


@router.patch("/{id}")
async def update(id: str):
    return {"msg": id}
