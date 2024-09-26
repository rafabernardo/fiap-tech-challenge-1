from db.mongodb.interfaces.queue import QueueRepositoryInterface
from models.queue import QueueItem


class QueueService:
    def __init__(self, repository: QueueRepositoryInterface):
        self.repository = repository

    def register_queue_item(self, queue_item: QueueItem) -> QueueItem:
        new_queue_item = self.repository.add(queue_item)
        return new_queue_item

    def get_queue_item_by_id(self, id: str) -> QueueItem | None:
        queue_item = self.repository.get_by_id(id)
        return queue_item

    def list_queue_items(
        self, filter: dict, page: int, page_size: int
    ) -> list[QueueItem]:
        paginated_queue_items = self.repository.list_queue_items(
            filter=filter, page=page, page_size=page_size
        )
        return paginated_queue_items

    def count_queue_items(self, filter: dict) -> int:
        total_queue_items = self.repository.count_queue_items(filter=filter)
        return total_queue_items
