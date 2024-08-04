from adapters.driven.repositories.utils import (
    prepare_document_to_db,
    replace_id_key,
)
from config.database import get_mongo_database
from core.domain.models.user import User
from core.domain.ports.repositories.user import UserRepositoryInterface


class UserMongoRepository(UserRepositoryInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Users"]

    def _add(self, user: User) -> User:
        user_data = user.model_dump()
        user_to_db = prepare_document_to_db(user_data)
        self.collection.insert_one(user_to_db)
        final_user = replace_id_key(user_to_db)

        return User(**final_user)

    def _get_by_id(self, id: int) -> User | None:
        query = self.get_user_by_id_query(id=id)
        user = self.collection.find_one(query)
        if user:
            return User(**user)
        return None

    def _list_users(self) -> list[User] | None:
        query = self.get_list_users_query()
        users = self.collection.find(query)
        if users:
            return [User(**replace_id_key(user)) for user in users]

        return None

    def _exists_by_cpf(self, cpf: str) -> bool:
        return self.collection.count_documents({"cpf": cpf}) > 0

    @staticmethod
    def get_user_by_id_query(id: int) -> dict:
        query = {"id": id}
        return query

    @staticmethod
    def get_list_users_query() -> dict:
        query = {}
        return query
