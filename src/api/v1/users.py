import traceback

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
    UnprocessableEntityErrorHTTPException,
)
from api.v1.models.user import (
    IdentifyUserV1Request,
    RegisterUserV1Request,
    UserV1Response,
)
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
from core.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from models.user import User
from services.user_service import UserService

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/users")


@router.get("", response_model=list[UserV1Response])
@inject
async def list_users(
    response: Response,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    try:
        users = user_service.list_users()
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return users


@router.get("/{id}", response_model=UserV1Response)
@inject
async def get_user_by_id(
    id: int,
    response: Response,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user = user_service.get_user_by_id(id)
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    if not user:
        raise NoDocumentsFoundHTTPException()
    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return user


@router.get("/cpf/{cpf}", response_model=UserV1Response)
@inject
async def get_user_by_cpf(
    cpf: str,
    response: Response,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    try:
        user = user_service.get_user_by_cpf(cpf)

    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(
            detail=exc.message,
        )
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    if user is None:
        raise NoDocumentsFoundHTTPException()

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return user


@router.post("/register", response_model=UserV1Response)
@inject
async def register(
    create_user_request: RegisterUserV1Request,
    response: Response,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    user = User(**create_user_request.model_dump())
    try:
        created_user = user_service.register_user(user)
    except UserAlreadyExistsError as exc:
        raise NoDocumentsFoundHTTPException(detail=exc.message)
    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(detail=exc.message)
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_user


@router.delete("/delete/{id}")
@inject
async def delete(
    id: int,
    response: Response,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    try:
        was_user_deleted = user_service.delete_user(id)

        if was_user_deleted:
            response.status_code = status.HTTP_204_NO_CONTENT
            return

        raise InternalServerErrorHTTPException()

    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()


@router.patch("/identify/{id}", response_model=UserV1Response)
@inject
async def identify_user(
    id: int,
    identify_user_request: IdentifyUserV1Request,
    response: Response,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    try:

        updated_user = user_service.identify_user(
            id, identify_user_request.cpf
        )

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return updated_user

    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(exc.message)
    except UserAlreadyExistsError as exc:
        raise UnprocessableEntityErrorHTTPException(exc.message)
    except Exception:
        print(traceback.format_exc())
        raise InternalServerErrorHTTPException()
