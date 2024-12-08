from core.exceptions.commons_exceptions import DataConflictException
from db.interfaces.order import OrderRepositoryInterface
from db.postgresql.database import get_postgresql_session
from db.postgresql.models.order import OrderModel
from db.postgresql.models.order_product import OrderProductModel
from models.order import Order, OrderFilter, OrderItem
from sqlalchemy import delete, func, insert, update
from sqlalchemy.future import select


class OrderPostgresRepository(OrderRepositoryInterface):
    def __init__(self):
        self.db_session = get_postgresql_session

    def _add(self, order: Order):
        with self.db_session() as session:
            db_order = session.execute(
                select(OrderModel).where(OrderModel.id == order.id)
            )
            if db_order:
                raise DataConflictException("Order already exists")
            session.execute(insert(OrderModel).values(**order.model_dump()))
            session.commit()

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
                    *[getattr(OrderModel, key).asc() for key in sort.get("asc", [])],
                    *[getattr(OrderModel, key).desc() for key in sort.get("desc", [])],
                )
            query = query.offset(page * page_size).limit(page_size)
            db_orders = session.execute(query).scalars().all()
        return [Order.model_validate(db_order) for db_order in db_orders]

    def _count_orders(self, order_filter: OrderFilter) -> int:
        with self.db_session() as session:
            query = (
                select(func.count())
                .select_from(OrderModel)
                .where(
                    OrderModel.status == order_filter.status
                )
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
                select(func.count()).select_from(OrderModel).where(OrderModel.id == id)
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
            query = select(OrderProductModel).where(OrderProductModel.order_id == id)
            db_order_items = session.execute(query)
        return [
            OrderItem.model_validate(db_order_item) for db_order_item in db_order_items
        ]
