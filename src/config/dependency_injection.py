from dependency_injector import containers, providers

from adapters.driven.repositories.order_repository import OrderMongoRepository
from adapters.driven.repositories.product_repository import (
    ProductMongoRepository,
)
from adapters.driven.repositories.queue_repository import QueueMongoRepository
from adapters.driven.repositories.user_repository import UserMongoRepository
from core.application.services.order_service import OrderService
from core.application.services.product_service import ProductService
from core.application.services.queue_service import QueueService
from core.application.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["adapters.driver.entrypoints.v1.orders"]
    )
    order_repository = providers.Factory(OrderMongoRepository)
    order_service = providers.Factory(OrderService, order_repository)

    product_repository = providers.Factory(ProductMongoRepository)
    product_service = providers.Factory(ProductService, product_repository)

    queue_repository = providers.Factory(QueueMongoRepository)
    queue_service = providers.Factory(QueueService, queue_repository)

    user_repository = providers.Factory(UserMongoRepository)
    user_service = providers.Factory(UserService, user_repository)
