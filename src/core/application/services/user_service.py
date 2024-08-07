from core.application.exceptions.commons_exceptions import (
    NoDocumentsFoundException,
)
from core.application.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from core.application.services.utils import clean_cpf_to_db
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

            user.cpf = clean_cpf_to_db(user.cpf)

        return self.repository.add(user)

    def get_user_by_cpf(self, cpf: str) -> User:
        valid_cpf = validate_cpf(cpf)
        if not valid_cpf:
            raise UserInvalidFormatDataError("Invalid CPF format")

        clean_cpf = clean_cpf_to_db(cpf)
        return self.repository.get_by_cpf(clean_cpf)

    def delete_user(self, id: str) -> bool:
        user_exists = self.repository.exists_by_id(id)
        if not user_exists:
            raise NoDocumentsFoundException()

        return self.repository.delete_order(id)

    def identify_user(self, id: str, cpf: str) -> User:
        user_exists = self.repository.exists_by_id(id)
        if not user_exists:
            raise NoDocumentsFoundException()

        valid_cpf = validate_cpf(cpf)
        if valid_cpf:
            clean_cpf = clean_cpf_to_db(cpf)
            return self.repository.update_user(id, cpf=clean_cpf)

        raise UserInvalidFormatDataError("Invalid CPF format")
