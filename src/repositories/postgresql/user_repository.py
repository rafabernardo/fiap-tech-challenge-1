import copy
from datetime import datetime

from db.postgresql.database import get_postgresql_session
from db.postgresql.models.user import UserModel
from models.user import User
from repositories.utils import prepare_document_to_db
from sqlalchemy.exc import NoResultFound


class UserPostgresRepository:
    def __init__(self):
        """
        Initialize the repository with a database session.
        If no session is provided, use the default session factory.
        """
        self.db_session = get_postgresql_session

    def add(self, user: User) -> User:
        """
        Add a new user to the database.
        """
        user_data = user.model_dump()
        user_to_db = prepare_document_to_db(user_data)
        user_model = UserModel(**user_to_db)
        with self.db_session() as session:
            session.add(user_model)
            session.commit()
            session.refresh(user_model)
        return self.convert_user_model(user_model)

    def get_by_id(self, user_id: str) -> User | None:
        """
        Fetch a user by their ID.
        """
        try:
            with self.db_session() as session:
                user = session.query(UserModel).filter_by(id=user_id).one()
            return self.convert_user_model(user)

        except NoResultFound:
            return None

    def list_users(self) -> list[User]:
        """
        List all users in the database.
        """
        with self.db_session() as session:
            users = session.query(UserModel).all()
        return [self.convert_user_model(user) for user in users]

    def exists_by_cpf(self, cpf: str) -> bool:
        """
        Check if a user exists by their CPF.
        """
        with self.db_session() as session:
            return session.query(UserModel).filter_by(cpf=cpf).count() > 0

    def exists_by_id(self, user_id: str) -> bool:
        """
        Check if a user exists by their ID.
        """
        with self.db_session() as session:
            return session.query(UserModel).filter_by(id=user_id).count() > 0

    def get_by_cpf(self, cpf: str) -> User | None:
        """
        Fetch a user by their CPF.
        """
        try:
            with self.db_session() as session:
                user = session.query(UserModel).filter_by(cpf=cpf).one()
            return self.convert_user_model(user)
        except NoResultFound:
            return None

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by their ID.
        """
        with self.db_session() as session:
            print("adasd")
            result = session.query(UserModel).where(UserModel.id == user_id).delete()
            session.commit()
        return result > 0

    def update_user(self, user_id: str, **kwargs) -> User | None:
        """
        Update a user's information by their ID.
        """
        kwargs["updated_at"] = (
            datetime.now()
        )
        with self.db_session() as session:
            result = session.query(UserModel).filter(UserModel.id == user_id).update(kwargs)
            session.commit()
        if result:
            return self.get_by_id(user_id)
        return None

    def close(self):
        """
        Close the database session.
        """
        self.db_session().close()

    @staticmethod
    def convert_user_model(user_model: UserModel) -> User:
        data = copy.deepcopy(user_model.__dict__)
        data["id"] = str(data["id"])
        return User.model_validate(data)