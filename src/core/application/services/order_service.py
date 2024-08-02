from core.domain.models.order import Order
from core.domain.ports.repositories.order import OrderRepositoryInterface


class OrderService:
    def __init__(self, repository: OrderRepositoryInterface):
        self.repository = repository

    def register_order(self, order: Order) -> Order:
        new_order = self.repository.add(order)
        return new_order
