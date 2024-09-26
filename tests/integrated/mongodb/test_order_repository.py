from datetime import datetime

from models.order import Order
from repositories.order_repository import OrderMongoRepository

if __name__ == "__main__":

    order_repository = OrderMongoRepository()
    orders = order_repository.list_orders()
    now = datetime.now()
    result = order_repository.add(
        Order(
            id="PRA QUEBRAR",
            status="pending",
            products=[],
            # created_at=now,
            # updated_at=now,
            # owner= None,
            payment_status="pending",
        )
    )
    result.status = "confirmed"
    order_repository.update_order(result)
    print(result)
    orders = order_repository.list_orders()
    print(orders)
    order_by_id = order_repository.get_by_id(result.id)
    print(order_by_id)
