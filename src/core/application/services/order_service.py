import copy

from core.application.exceptions.commons_exceptions import (
    DataConflictException,
    NoDocumentsFoundException,
)
from core.application.services.order_number_service import OrderNumberService
from core.domain.models.order import Order, OrderFilter, PaymentStatus
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
        self, order_filter: OrderFilter, page: int, page_size: int
    ) -> list[Order]:
        paginated_orders = self.repository.list_orders(
            order_filter=order_filter, page=page, page_size=page_size
        )
        return paginated_orders

    def count_orders(self, order_filter: OrderFilter) -> int:
        total_orders = self.repository.count_orders(order_filter=order_filter)
        return total_orders

    def delete_order(self, id: str) -> bool:
        order = self.get_order_by_id(id)
        if order is None:
            raise NoDocumentsFoundException()
        was_order_deleted = self.repository.delete_order(id=id)
        return was_order_deleted

    def set_payment_status(self, id: str, payment_result: bool):

        order = self.repository.get_by_id(id)
        if not order:
            raise NoDocumentsFoundException()
        if PaymentStatus(order.payment_status) is not PaymentStatus.pending:
            raise DataConflictException()

        new_payment_status = (
            PaymentStatus.paid if payment_result else PaymentStatus.canceled
        )
        updated_order = self.repository.update_order(
            id, payment_status=new_payment_status.value
        )
        return updated_order

    def prepare_new_order(
        self, order_data: dict, products_data: list[dict]
    ) -> Order:
        order_data_copy = copy.deepcopy(order_data)
        total_price = sum(
            [
                product_data.get("price")
                for product_data in products_data
                if isinstance(product_data.get("price"), int)
            ]
        )
        order_data_copy.update(
            {
                "products": products_data,
                "total_price": total_price,
                "status": order_data_copy.get("status", "pending"),
                "payment_status": order_data_copy.get(
                    "payment_status", "pending"
                ),
            }
        )
        new_order = Order(**order_data_copy)
        return new_order
