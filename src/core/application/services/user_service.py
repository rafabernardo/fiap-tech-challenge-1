from core.application.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
    UserNotFoundError,
)
from core.application.validators.user import validate_cpf, validate_email
from core.domain.models.user import User
from core.domain.ports.repositories.user import UserRepositoryInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def register_user(self, user: User) -> User:
        valid_email = validate_email(user.email)
        valid_cpf = validate_cpf(user.cpf)

        if not valid_email:
            raise UserInvalidFormatDataError("Invalid email format")
        if user.cpf:
            if not valid_cpf:
                raise UserInvalidFormatDataError("Invalid CPF format")
            if self.repository.exists_by_cpf(user.cpf):
                raise UserAlreadyExistsError(
                    "A user with this CPF already exists"
                )

        return self.repository.add(user)

    def get_user_by_cpf(self, cpf: str) -> User:
        valid_cpf = validate_cpf(cpf)
        if not valid_cpf:
            raise UserInvalidFormatDataError("Invalid CPF format")

        return self.repository.get_by_cpf(cpf)

    def delete_user(self, id: str) -> bool:
        user_exists = self.repository.exists_by_id(id)
        if not user_exists:
            raise UserNotFoundError()

        return self.repository.delete_order(id)
