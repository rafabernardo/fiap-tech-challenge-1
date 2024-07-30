from adapters.driven.repositories.user_repository import UserMongoRepository
from core.domain.models.user import User

if __name__ == "__main__":
    user_repository = UserMongoRepository()
    users = user_repository.list_users()

    user_repository.add(
        User(
            id=1234,
            name="Kiki Ki",
            email="kiki_gatinha@gmiau.com",
            cpf="11223344",
        )
    )
    users = user_repository.list_users()
    print(users)
    kiki = user_repository.get_by_id(id=1234)
    print(kiki)
