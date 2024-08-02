from bson import ObjectId
from pymongo import ReturnDocument

from adapters.driven.repositories.utils import (
    prepare_document_to_db,
    replace_id_key,
)
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
        order_to_db = prepare_document_to_db(order_data)
        self.collection.insert_one(order_to_db)

        final_order = order_to_db
        replace_id_key(final_order)
        return Order(**final_order)

    def _get_by_id(self, id: str) -> Order | None:
        query = self.get_order_by_id_query(id=id)
        order: dict = self.collection.find_one(query)
        if not order:
            return None

        replace_id_key(order)
        return Order(**order)

    def _list_orders(self) -> list[Order] | None:
        query = self.get_list_orders_query()
        orders = list(self.collection.find(query))
        if not orders:
            return None
        return [Order(**replace_id_key(order)) for order in orders]

    def _update_order(self, order: Order) -> Order:
        order_data = order.model_dump()
        order_to_db = prepare_document_to_db(order_data)

        order_filter = self.get_order_by_id_query(order.id)
        order_update_data = self.get_order_update_data(order_to_db)
        updated_order = self.collection.find_one_and_update(
            filter=order_filter,
            update=order_update_data,
            return_document=ReturnDocument.AFTER,
        )

        replace_id_key(updated_order)
        return Order(**updated_order)

    def _add_order_item(self, id, order_item: OrderItem) -> None:
        raise NotImplementedError

    def _list_order_items_by_order_id(self, id) -> list[OrderItem]:
        raise NotImplementedError

    @staticmethod
    def get_order_by_id_query(id: str) -> dict:
        query = {"_id": ObjectId(id)}
        return query

    @staticmethod
    def get_order_update_data(data: dict) -> dict:
        order_update_data = {"$set": data}
        return order_update_data

    @staticmethod
    def get_list_orders_query() -> dict:
        query = {}
        return query