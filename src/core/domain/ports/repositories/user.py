import abc

from core.domain.models.user import User


class UserRepositoryInterface(abc.ABC):

    def __init__(self): ...

    def add(self, user: User) -> User:
        user = self._add(user)
        return user

    def get_by_id(self, id: str) -> User:
        user = self._get_by_id(id)
        return user

    def exists_by_cpf(self, cpf: str) -> bool:
        return self._exists_by_cpf(cpf)

    def exists_by_id(self, id: str) -> bool:
        return self._exists_by_id(id)

    def list_users(self) -> list[User]:
        users = self._list_users()
        return users

    def get_by_cpf(self, cpf: str) -> User:
        user = self._get_by_cpf(cpf)
        return user

    def delete_order(self, id: str) -> bool:
        return self._delete_user(id)

    def update_user(self, id: str, **kwargs) -> User:
        user = self._update_user(id, **kwargs)
        return user

    @abc.abstractmethod
    def _add(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _exists_by_cpf(self, cpf: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _exists_by_id(self, id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_users(self) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_cpf(self, cpf: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_user(self, id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_user(self, id: str, **kwargs) -> User:
        raise NotImplementedError
