import abc

from core.domain.models.order import Order, OrderItem


class OrderRepositoryInterface(abc.ABC):
    def __init__(self): ...

    def add(self, order: Order) -> Order:
        new_order = self._add(order)
        return new_order

    def get_by_id(self, id: str) -> Order:
        order = self._get_by_id(id)
        return order

    def list_orders(
        self, filter: dict, page: int, page_size: int
    ) -> list[Order]:
        orders = self._list_orders(
            filter=filter, page=page, page_size=page_size
        )
        return orders

    def count_orders(self, filter: dict) -> int:
        total_orders = self._count_orders(filter=filter)
        return total_orders

    def delete_order(self, id: str) -> bool:
        was_order_deleted = self._delete_order(id=id)
        return was_order_deleted

    def update_order(self, id: str, **kwargs) -> Order:
        order = self._update_order(id, **kwargs)
        return order

    def add_order_item(self, id: str, order_item: OrderItem) -> None:
        self._add_order_item(id, order_item)
        # self.seen.add(_add_order_item) # Add Order ??

    def list_order_items_by_order_id(self, id) -> list[OrderItem]:
        order_items = self._list_order_items_by_order_id(id)
        # if order_items:
        #     self.seen.union(set(users)) # Add Order ??
        return order_items

    @abc.abstractmethod
    def _add(self, order: Order) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: str) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_orders(
        self, filter: dict, page: int, page_size: int
    ) -> list[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def _count_orders(self, filter: dict) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_order(self, id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_order(self, id: str, **kwargs) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_order_item(self, id: str, order_item: OrderItem) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_order_items_by_order_id(self, id) -> list[OrderItem]:
        raise NotImplementedError
