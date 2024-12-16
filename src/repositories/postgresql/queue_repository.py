from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from db.interfaces.queue import QueueRepositoryInterface
from db.postgresql.database import get_postgresql_session
from db.postgresql.models.queue_item import QueueItemModel
from models.queue import QueueItem
from repositories.utils import prepare_document_to_db


class QueueRepositoryInterface(QueueRepositoryInterface):
    def __init__(self):
        self.db_session = get_postgresql_session

    def _add(self, queue_item: QueueItem) -> QueueItem:
        queue_data = queue_item.model_dump()
        queue_to_db = prepare_document_to_db(queue_data)
        new_queue = QueueItemModel(**queue_to_db)
        with self.db_session() as session:
            session.add(new_queue)
            session.commit()
            session.refresh(new_queue)
        return QueueItem

    def _get_by_id(self, id: str) -> QueueItem:
        try:
            with self.db_session() as session:
                queue_item = session.query(QueueItemModel).filter_by(id=id).one()
            return QueueItem(**queue_item.__dict__)
        except NoResultFound:
            return None

    def _get_by_order_id(self, id: str) -> QueueItem:
        try:
            with self.db_session() as session:
                queue_item = session.query(QueueItemModel).filter_by(order_id=id).one()
            return QueueItem(**queue_item.__dict__)
        except NoResultFound:
            return None

    def _list_queue_items(
        self, filter: dict, page: int, page_size: int
    ) -> list[QueueItem]:
        skip = (page - 1) * page_size
        query = (
            select(QueueItemModel)
            .filter_by(**filter)
            .offset(skip)
            .limit(page_size)
        )
        with self.db_session() as session:
            result = session.execute(query).scalars().all()
        return [QueueItem(**queue_item.__dict__) for queue_item in result]


    def _count_queue_items(self, filter: dict) -> int:
        query = select(QueueItemModel).filter_by(**filter)
        with self.db_session() as session:
            result = session.execute(query).scalars().all()
        return len(result)
    
    def _delete_queue_item(self, id: str) -> bool:
        query = delete(QueueItemModel).where(QueueItemModel.id == id)
        with self.db_session() as session:
            result = session.execute(query)
            session.commit()
        return result.rowcount > 0