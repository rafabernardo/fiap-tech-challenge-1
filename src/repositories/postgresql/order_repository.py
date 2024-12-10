from sqlalchemy import delete, func, insert, update
from sqlalchemy.future import select

from core.exceptions.commons_exceptions import DataConflictException
from db.interfaces.order import OrderRepositoryInterface
from db.postgresql.database import get_postgresql_session
from db.postgresql.models.order import OrderModel
from db.postgresql.models.order_product import OrderProductModel
from models.order import Order, OrderFilter, OrderItem
from repositories.utils import prepare_document_to_db


class OrderPostgresRepository(OrderRepositoryInterface):
    def __init__(self):
        self.db_session = get_postgresql_session

    def _add(self, order: Order) -> Order:
        with self.db_session() as session:
            db_order = session.execute(
                select(OrderModel).where(OrderModel.id == order.id)
            ).first()
            if db_order:
                raise DataConflictException("Order already exists")
            order_data = order.model_dump()
            order_data_to_db = prepare_document_to_db(order_data)
            new_order = OrderModel(
                status=order_data_to_db["status"],
                created_at=order_data_to_db["created_at"],
                updated_at=order_data_to_db["updated_at"],
                order_number=order_data_to_db["order_number"],
                owner_id=order_data_to_db["owner_id"],
                payment_status=order_data_to_db["payment_status"],
                paid_at=order_data_to_db["paid_at"],
                total_price=order_data_to_db["total_price"],
            )
            session.add(new_order)
            session.commit()
            session.refresh(new_order)

            for product in order.products:
                order_product = OrderProductModel(
                    order_id=new_order.id,
                    product_id=product.product.id,
                    quantity=product.quantity,
                    price=product.price,
                )
                session.add(order_product)

            session.commit()
            order.id = new_order.id
            order.updated_at = new_order.updated_at
            order.created_at = new_order.created_at
            return order

    def _get_by_id(self, id: str) -> Order | None:
        with self.db_session() as session:
            db_order = session.execute(
                select(OrderModel).where(OrderModel.id == id)
            ).first()
        if not db_order:
            return None
        return Order.model_validate(db_order)

    def _list_orders(
        self, order_filter: OrderFilter, page: int, page_size: int, sort: dict
    ) -> list[Order]:
        with self.db_session() as session:
            query = select(OrderModel)
            if order_filter.status:
                query = query.where(OrderModel.status.in_(order_filter.status))
            if sort:
                query = query.order_by(
                    *[
                        getattr(OrderModel, key).asc()
                        for key in sort.get("asc", [])
                    ],
                    *[
                        getattr(OrderModel, key).desc()
                        for key in sort.get("desc", [])
                    ],
                )
            query = query.offset(page * page_size).limit(page_size)
            db_orders = session.execute(query).scalars().all()
        return [Order.model_validate(db_order) for db_order in db_orders]

    def _count_orders(self, order_filter: OrderFilter) -> int:
        with self.db_session() as session:
            query = (
                select(func.count())
                .select_from(OrderModel)
                .where(OrderModel.status == order_filter.status)
            )
            result = session.execute(query).scalar()
        return result

    def _delete_order(self, id: str):
        with self.db_session() as session:
            session.execute(delete(OrderModel).where(OrderModel.id == id))
            session.commit()

    def _update_order(self, id: str, **kwargs):
        with self.db_session() as session:
            session.execute(
                update(OrderModel).where(OrderModel.id == id).values(**kwargs)
            )
            session.commit()

    def _exists_by_id(self, id: str) -> bool:
        with self.db_session() as session:
            result = session.scalar(
                select(func.count())
                .select_from(OrderModel)
                .where(OrderModel.id == id)
            )
        return bool(result)

    def _add_order_item(self, id: str, order_item: OrderItem):
        with self.db_session() as session:
            session.execute(
                insert(OrderProductModel).values(
                    order_id=id,
                    product_id=order_item.product_id,
                    quantity=order_item.quantity,
                )
            )
            session.commit()

    def _list_order_items_by_order_id(self, id: str) -> list[OrderItem]:
        with self.db_session() as session:
            query = select(OrderProductModel).where(
                OrderProductModel.order_id == id
            )
            db_order_items = session.execute(query)
        return [
            OrderItem.model_validate(db_order_item)
            for db_order_item in db_order_items
        ]
