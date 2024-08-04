from fastapi import APIRouter, HTTPException, Response, status

from adapters.driven.repositories.order_repository import OrderMongoRepository
from adapters.driver.entrypoints.v1.models.order import (
    RegisterOrderV1Request,
    RegisterOrderV1Response,
)
from core.application.services.order_service import OrderService
from core.domain.models.order import Order

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/order")


@router.get("")
async def list_users():
    return {"msg": "pong"}


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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
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
