from dependency_injector import containers, providers

from repositories.postgresql.order_repository import OrderPostgresRepository
from repositories.postgresql.product_repository import (
    ProductPostgresRepository,
)
from repositories.postgresql.user_repository import UserPostgresRepository
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
    order_repository = providers.Factory(OrderPostgresRepository)
    order_service = providers.Factory(OrderService, order_repository)

    product_repository = providers.Factory(ProductPostgresRepository)
    product_service = providers.Factory(ProductService, product_repository)

    queue_repository = providers.Factory()
    queue_service = providers.Factory(QueueService, queue_repository)

    user_repository = providers.Factory(UserPostgresRepository)
    user_service = providers.Factory(UserService, user_repository)
