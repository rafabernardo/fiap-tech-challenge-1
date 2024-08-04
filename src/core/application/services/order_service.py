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

    def get_order_by_id(self, id: str) -> Order:
        order = self.repository.get_by_id(id)
        return order

    def list_orders(
        self, filter: dict, page: int, page_size: int
    ) -> list[Order]:
        paginated_orders = self.repository.list_orders(
            filter=filter, page=page, page_size=page_size
        )
        return paginated_orders

    def count_orders(self, filter: dict) -> int:
        total_orders = self.repository.count_orders(filter=filter)
        return total_orders

    def delete_order(self, id: str) -> bool:
        was_order_deleted = self.repository.delete_order(id=id)
        return was_order_deleted
