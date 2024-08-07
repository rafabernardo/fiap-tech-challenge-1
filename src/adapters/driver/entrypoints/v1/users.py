from fastapi import APIRouter, Response, status

from adapters.driven.repositories.user_repository import UserMongoRepository
from adapters.driver.entrypoints.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
    UnprocessableEntityErrorHTTPException,
)
from adapters.driver.entrypoints.v1.models.user import (
    IdentifyUserV1Request,
    RegisterUserV1Request,
    UserV1Response,
)
from core.application.exceptions.commons_exceptions import (
    NoDocumentsFoundException,
)
from core.application.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from core.application.services.user_service import UserService
from core.domain.models.user import User

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/users")


@router.get("", response_model=list[UserV1Response])
async def list_users(
    response: Response,
):

    user_repository = UserMongoRepository()
    try:
        users = user_repository.list_users()
    except Exception:
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return users


@router.get("/{id}", response_model=UserV1Response)
async def get_user_by_id(
    id: str,
    response: Response,
):
    user_repository = UserMongoRepository()
    try:
        user = user_repository.get_by_id(id)

    except Exception:
        raise InternalServerErrorHTTPException()

    if not user:
        raise NoDocumentsFoundHTTPException()
    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return user


@router.get("/cpf/{cpf}", response_model=UserV1Response)
async def get_user_by_cpf(
    cpf: str,
    response: Response,
):
    user_repository = UserMongoRepository()
    service = UserService(user_repository)
    try:
        user = service.get_user_by_cpf(cpf)

    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(
            detail=exc.message,
        )
    except Exception:
        raise InternalServerErrorHTTPException()

    if user is None:
        raise NoDocumentsFoundHTTPException()

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return user


@router.post("/register", response_model=UserV1Response)
async def register(
    create_user_request: RegisterUserV1Request,
    response: Response,
):
    user_repository = UserMongoRepository()
    service = UserService(user_repository)
    user = User(**create_user_request.model_dump())
    try:
        created_user = service.register_user(user)
    except UserAlreadyExistsError as exc:
        raise NoDocumentsFoundHTTPException(detail=exc.message)
    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(detail=exc.message)
    except Exception:
        raise InternalServerErrorHTTPException()

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_user


@router.delete("/delete/{id}")
async def delete(
    id: str,
    response: Response,
):
    user_repository = UserMongoRepository()
    service = UserService(user_repository)

    try:
        was_user_deleted = service.delete_user(id)

        if was_user_deleted:
            response.status_code = status.HTTP_204_NO_CONTENT
            return

        raise InternalServerErrorHTTPException()

    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except Exception:
        raise InternalServerErrorHTTPException()


@router.patch("/identify/{id}", response_model=UserV1Response)
async def identify_user(
    id: str,
    identify_user_request: IdentifyUserV1Request,
    response: Response,
):
    user_repository = UserMongoRepository()
    service = UserService(user_repository)

    try:

        updated_user = service.identify_user(id, identify_user_request.cpf)

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return updated_user

    except NoDocumentsFoundException:
        raise NoDocumentsFoundHTTPException()
    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(exc.message)
    except Exception:
        InternalServerErrorHTTPException
