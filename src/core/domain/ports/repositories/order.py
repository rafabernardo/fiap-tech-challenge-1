import abc

from core.domain.models.order import Order, OrderItem


class OrderRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen: set[Order] = set()

    def add(self, order: Order) -> None:
        self._add(order)
        self.seen.add(order)

    def get_by_id(self, id: int) -> Order:
        order = self._get_by_id(id)
        if order:
            self.seen.add(order)
        return order

    def list_orders(self) -> list[Order]:
        orders = self._list_orders()
        if orders:
            self.seen.union(set(orders))
        return orders

    def add_order_item(self, id, order_item: OrderItem) -> None:
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
    def _get_by_id(self, id: int) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_orders(self) -> list[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_order_item(self, id, order_item: OrderItem) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_order_items_by_order_id(self, id) -> list[OrderItem]:
        raise NotImplementedError