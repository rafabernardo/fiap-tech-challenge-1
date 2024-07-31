from bson import ObjectId

from adapters.driven.repositories.utils import replace_id_key
from config.database import get_mongo_database
from core.domain.models.order import Order, OrderItem
from core.domain.ports.repositories.order import OrderRepositoryInterface


class OrderMongoRepository(OrderRepositoryInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Order"]
        super().__init__()

    def _add(self, order: Order) -> Order:
        order_data = order.model_dump()
        if order_id := order_data.get("id"):
            raise Exception(f"There is already an Order with id {order_id}")
        order_data.pop("id")
        result = self.collection.insert_one(order_data)
        result_id = str(result.inserted_id)

        order_data["id"] = result_id
        return Order(**order_data)

    def _get_by_id(self, id: str) -> Order | None:
        query = self.get_order_by_id_query(id=id)
        order: dict = self.collection.find_one(query)
        if not order:
            return None
        replace_id_key(order)
        return Order(**order)

    def _list_orders(self) -> list[Order] | None:
        query = self.get_list_orders_query()
        orders = self.collection.find(query)
        replace_id_key(orders)
        if not orders:
            return None
        return [Order(**order) for order in orders]

    def _add_order_item(self, id, order_item: OrderItem) -> None:
        raise NotImplementedError

    def _list_order_items_by_order_id(self, id) -> list[OrderItem]:
        raise NotImplementedError

    @staticmethod
    def get_order_by_id_query(id: str) -> dict:
        query = {"_id": ObjectId(id)}
        return query

    @staticmethod
    def get_list_orders_query() -> dict:
        query = {}
        return query
