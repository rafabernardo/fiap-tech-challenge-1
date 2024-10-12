import abc

from models.order import Order, OrderFilter, OrderItem


class OrderRepositoryInterface(abc.ABC):
    def __init__(self): ...

    def add(self, order: Order) -> Order:
        new_order = self._add(order)
        return new_order

    def get_by_id(self, id: str) -> Order:
        order = self._get_by_id(id)
        return order

    def list_orders(
        self,
        order_filter: OrderFilter,
        page: int,
        page_size: int,
        sort: dict = None,
    ) -> list[Order]:
        orders = self._list_orders(
            order_filter=order_filter,
            page=page,
            page_size=page_size,
            sort=sort,
        )
        return orders

    def count_orders(self, order_filter: OrderFilter) -> int:
        total_orders = self._count_orders(order_filter=order_filter)
        return total_orders

    def delete_order(self, id: str) -> bool:
        was_order_deleted = self._delete_order(id=id)
        return was_order_deleted

    def exists_by_id(self, id: str) -> bool:
        return self._exists_by_id(id)

    def update_order(self, id: str, **kwargs) -> Order:
        order = self._update_order(id, **kwargs)
        return order

    def add_order_item(self, id: str, order_item: OrderItem) -> None:
        self._add_order_item(id, order_item)

    def list_order_items_by_order_id(self, id) -> list[OrderItem]:
        order_items = self._list_order_items_by_order_id(id)

        return order_items

    @abc.abstractmethod
    def _add(self, order: Order) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: str) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_orders(
        self, filter: OrderFilter, page: int, page_size: int, sort: dict = None
    ) -> list[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def _count_orders(self, filter: OrderFilter) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_order(self, id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_order(self, id: str, **kwargs) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def _exists_by_id(self, id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_order_item(self, id: str, order_item: OrderItem) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_order_items_by_order_id(self, id) -> list[OrderItem]:
        raise NotImplementedError
