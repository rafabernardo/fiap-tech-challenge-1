from core.application.exceptions.user_exceptions import UserAlreadyExistsError
from core.domain.models.user import User
from core.domain.ports.repositories.user import UserRepositoryInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(self, user: User) -> User:
        if user.cpf and self.repository.exists_by_cpf(user.cpf):
            raise UserAlreadyExistsError("A user with this CPF already exists")
        return self.repository.add(user)
