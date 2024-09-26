import copy
from datetime import datetime

from core.exceptions.commons_exceptions import (
    DataConflictException,
    NoDocumentsFoundException,
)
from db.mongodb.interfaces.order import OrderRepositoryInterface
from models.order import (
    Order,
    OrderFilter,
    OrderItem,
    OrderOutput,
    PaymentStatus,
    Status,
)
from services.order_number_service import OrderNumberService
from services.product_service import ProductService
from services.utils import get_seconds_diff

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
            return updated_order

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

    def update_order(self, id: str, **kwargs) -> Order:
        order = self.repository.exists_by_id(id)
        if not order:
            raise NoDocumentsFoundException()
        updated_order = self.repository.update_order(id, **kwargs)
        return updated_order

    def get_order_items_details(
        self, order_items: list[dict], product_service: ProductService
    ) -> list[OrderItem]:
        products_data = []
        for product in order_items:
            product_id = product.get("product_id")
            quantity = product.get("quantity")

            found_product = product_service.get_product_by_id(product_id)
            price = quantity * found_product.price
            products_data.append(
                OrderItem(
                    product=found_product.model_dump(),
                    quantity=quantity,
                    price=price,
                ).model_dump()
            )
        return products_data


def is_order_in_queue(status: Status) -> bool:
    return Status(status) in [
        Status.confirmed,
        Status.being_prepared,
        Status.received,
    ]


def prepare_order_to_list(order: Order) -> OrderOutput:
    order_response = OrderOutput(**order.model_dump())
    if is_order_in_queue(order.status) and order.paid_at is not None:
        order_response.waiting_time = get_seconds_diff(order.paid_at)
    return order_response
