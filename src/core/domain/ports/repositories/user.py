import abc

from core.domain.models.user import User


class UserRepositoryInterface(abc.ABC):

    def __init__(self):
        ...

    def add(self, user: User) -> None:
        self._add(user)

    def get_by_id(self, id: int) -> User:
        user = self._get_by_id(id)
        return user

    def list_users(self) -> list[User]:
        users = self._list_users()
        return users

    @abc.abstractmethod
    def _add(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_users(self) -> list[User]:
        raise NotImplementedError
