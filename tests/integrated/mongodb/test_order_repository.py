from datetime import datetime

from adapters.driven.repositories.order_repository import OrderMongoRepository
from core.domain.models.order import Order

if __name__ == "__main__":

    order_repository = OrderMongoRepository()
    now = datetime.now()
    result = order_repository.add(
        Order(
            # id="PRA QUEBRAR",
            status="pending",
            products=[],
            created_at=now,
            updated_at=now,
            # owner= None,
            payment_status="pending",
        )
    )
    print(result)
    orders = order_repository.list_orders()
    print(orders)
    order_by_id = order_repository.get_by_id(result.id)
    print(order_by_id)
