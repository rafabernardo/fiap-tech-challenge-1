from adapters.driven.repositories.order_repository import OrderMongoRepository
from adapters.driven.repositories.product_repository import (
    ProductMongoRepository,
)
from adapters.driven.repositories.user_repository import UserMongoRepository
from core.application.services.order_service import OrderService
from core.application.services.product_service import ProductService
from core.application.services.user_service import UserService


def get_order_service() -> OrderService:
    order_repository = OrderMongoRepository()
    order_service = OrderService(order_repository)
    return order_service


def get_product_service() -> ProductService:
    product_repository = ProductMongoRepository()
    product_service = ProductService(product_repository)
    return product_service


def get_user_service() -> UserService:
    user_repository = UserMongoRepository()
    user_service = UserService(user_repository)
    return user_service
