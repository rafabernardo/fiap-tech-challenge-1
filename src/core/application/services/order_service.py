from core.application.services.order_number_service import OrderNumberService
from core.domain.models.order import Order
from core.domain.ports.repositories.order import OrderRepositoryInterface

order_number_service = OrderNumberService()


class OrderService:
    def __init__(self, repository: OrderRepositoryInterface):
        self.repository = repository

    def register_order(self, order: Order) -> Order:
        order.order_number = order_number_service.get_next_order_number()
        new_order = self.repository.add(order)
        return new_order
