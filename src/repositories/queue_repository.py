from bson import ObjectId

from db.mongodb.database import get_mongo_database
from db.mongodb.interfaces.queue import QueueRepositoryInterface
from models.queue import QueueItem
from repositories.utils import prepare_document_to_db, replace_id_key


class QueueMongoRepository(QueueRepositoryInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Queue"]
        super().__init__()

    def _add(self, queue_item: QueueItem) -> QueueItem:
        queue_item_data = queue_item.model_dump()
        queue_item_to_db = prepare_document_to_db(queue_item_data)
        self.collection.insert_one(queue_item_to_db)

        final_queue_item = queue_item_to_db
        final_queue_item = replace_id_key(final_queue_item)
        return QueueItem(**final_queue_item)

    def _get_by_id(self, id: str) -> QueueItem | None:
        query = self.get_queue_item_by_id_query(id=id)
        queue_item: dict = self.collection.find_one(query)
        if not queue_item:
            return None

        queue_item = replace_id_key(queue_item)
        return QueueItem(**queue_item)

    def _list_queue_items(
        self, filter: dict, page: int, page_size: int
    ) -> list[QueueItem] | None:
        skip = (page - 1) * page_size
        queue_items = list(
            self.collection.find(filter).skip(skip).limit(page_size)
        )
        return [
            QueueItem(**replace_id_key(queue_item))
            for queue_item in queue_items
        ]

    def _count_queue_items(self, filter: dict) -> int:
        return self.collection.count_documents(filter)

    @staticmethod
    def get_queue_item_by_id_query(id: str) -> dict:
        query = {"_id": ObjectId(id)}
        return query

    @staticmethod
    def get_list_queue_items_query() -> dict:
        query = {}
        return query
