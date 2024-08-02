from fastapi import APIRouter, HTTPException, Response, status

from adapters.driven.repositories.user_repository import UserMongoRepository
from adapters.driver.entrypoints.v1.models.user import RegisterUserV1Request
from core.application.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from core.application.services.user_service import UserService
from core.domain.models.user import User

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/users")


@router.get("")
async def list_users():
    return {"msg": "pong"}


@router.get("/{id}")
async def get_user_by_id(id: int):
    return {"msg": id}


@router.get("/cpf/{cpf}")
async def get_user_by_cpf(cpf: str):
    return {"msg": cpf}


@router.post("/register")
async def register(
    create_user_request: RegisterUserV1Request,
    response: Response,
):
    user_repository = UserMongoRepository()
    service = UserService(user_repository)
    user = User(**create_user_request.model_dump())
    try:
        created_user = service.register_user(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
    except UserInvalidFormatDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_user


@router.delete("/delete/{id}")
async def delete(id: int):
    return {"msg": id}


@router.patch("/{id}")
async def update(id: int):
    return {"msg": id}
