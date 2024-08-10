import abc

from core.domain.models.queue import QueueItem


class QueueRepositoryInterface(abc.ABC):
    def __init__(self): ...

    def add(self, queue_item: QueueItem) -> QueueItem:
        new_queue_item = self._add(queue_item)
        return new_queue_item

    def get_by_id(self, id: str) -> QueueItem:
        queue_item = self._get_by_id(id)
        return queue_item

    def list_queue_items(
        self, filter: dict, page: int, page_size: int
    ) -> list[QueueItem]:
        queue_items = self._list_queue_items(
            filter=filter, page=page, page_size=page_size
        )
        return queue_items

    def count_queue_items(self, filter: dict) -> int:
        total_queue_items = self._count_queue_items(filter=filter)
        return total_queue_items

    @abc.abstractmethod
    def _add(self, queue_item: QueueItem) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: str) -> QueueItem:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_queue_items(
        self, filter: dict, page: int, page_size: int
    ) -> list[QueueItem]:
        raise NotImplementedError

    @abc.abstractmethod
    def _count_queue_items(self, filter: dict) -> int:
        raise NotImplementedError
