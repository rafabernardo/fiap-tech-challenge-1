from config.database import get_mongo_database
from core.domain.models.user import User
from core.domain.ports.repositories.user import UserRepositoryInterface


class UserMongoRepository(UserRepositoryInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Users"]

    def _add(self, user: User) -> None:
        self.collection.insert_one(user.model_dump())

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
            return [User(**user) for user in users]
        return None

    @staticmethod
    def get_user_by_id_query(id: int) -> dict:
        query = {"id": id}
        return query

    @staticmethod
    def get_list_users_query() -> dict:
        query = {}
        return query