from dependency_injector import containers, providers

from repositories.order_repository import OrderMongoRepository
from repositories.product_repository import ProductMongoRepository
from repositories.queue_repository import QueueMongoRepository
from repositories.user_repository import UserMongoRepository
from services.order_service import OrderService
from services.product_service import ProductService
from services.queue_service import QueueService
from services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.orders",
            "api.v1.products",
            "api.v1.users",
        ]
    )
    order_repository = providers.Factory(OrderMongoRepository)
    order_service = providers.Factory(OrderService, order_repository)

    product_repository = providers.Factory(ProductMongoRepository)
    product_service = providers.Factory(ProductService, product_repository)

    queue_repository = providers.Factory(QueueMongoRepository)
    queue_service = providers.Factory(QueueService, queue_repository)

    user_repository = providers.Factory(UserMongoRepository)
    user_service = providers.Factory(UserService, user_repository)
