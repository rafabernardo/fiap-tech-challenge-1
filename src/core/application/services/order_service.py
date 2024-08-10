from datetime import datetime

from core.application.exceptions.commons_exceptions import (
    DataConflictException,
    NoDocumentsFoundException,
)
from core.application.services.order_number_service import OrderNumberService
from core.application.services.utils import get_seconds_diff
from core.domain.models.order import (
    Order,
    OrderFilter,
    OrderOutput,
    PaymentStatus,
    Status,
)
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
    ) -> list[OrderOutput]:
        paginated_orders = self.repository.list_orders(
            order_filter=order_filter, page=page, page_size=page_size
        )

        listed_orders = [
            prepare_order_to_list(order) for order in paginated_orders
        ]

        return listed_orders

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

        if PaymentStatus(new_payment_status) is PaymentStatus.paid:
            updated_order = self.repository.update_order(
                id,
                payment_status=new_payment_status.value,
                paid_at=datetime.now(),
                status="confirmed",
            )

        updated_order = self.repository.update_order(
            id, payment_status=new_payment_status.value
        )

        return updated_order

    def prepare_new_order(self, new_order_data: dict) -> Order:
        new_order = Order(
            **new_order_data,
            status="pending",
            payment_status="pending",
        )
        return new_order

    from datetime import datetime


def is_order_being_prepared(status: Status) -> bool:
    return (
        Status(status) is Status.confirmed
        or Status(status) is Status.being_prepared
        or Status(status) is Status.received
    )


def prepare_order_to_list(order: Order) -> OrderOutput:
    if is_order_being_prepared(order.status):
        order_response = OrderOutput(**order.model_dump())
        order_response.waiting_time = get_seconds_diff(order.paid_at)
    return order_response
