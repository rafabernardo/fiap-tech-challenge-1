from sqlalchemy import delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from db.interfaces.product import ProductsRepositoryInterface
from db.postgresql.database import get_postgresql_session
from db.postgresql.models.product import ProductModel
from models.product import Product
from repositories.utils import prepare_document_to_db


class ProductPostgresRepository(ProductsRepositoryInterface):
    def __init__(self):
        self.db_session = get_postgresql_session

    def _add(self, product: Product) -> Product:
        product_data = product.model_dump()
        product_to_db = prepare_document_to_db(product_data)
        new_product = ProductModel(**product_to_db)
        with self.db_session() as session:
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
        return Product(**new_product.__dict__)

    def _get_by_id(self, id: str) -> Product | None:
        try:
            with self.db_session() as session:
                product = session.query(ProductModel).filter_by(id=id).one()
            return Product(**product.__dict__)
        except NoResultFound:
            return None

    def _list_products(
        self, filter: dict, page: int, page_size: int
    ) -> list[Product]:
        with self.db_session() as session:
            skip = (page - 1) * page_size
            query = (
                select(ProductModel)
                .filter_by(**filter)
                .offset(skip)
                .limit(page_size)
            )
            result = session.execute(query).scalars().all()
        return [Product(**product.__dict__) for product in result]

    def _count_products(self, filter: dict) -> int:
        with self.db_session() as session:
            query = select(ProductModel).filter_by(**filter)
            result = session.execute(query).scalars().all()
        return len(result)

    def _exists_by_id(self, id: str) -> bool:
        query = select(ProductModel).where(ProductModel.id == id)
        result = self.session.execute(query).scalar_one_or_none()
        return result is not None

    def _delete_product(self, id: str) -> bool:
        query = delete(ProductModel).where(ProductModel.id == id)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def _update_product(self, id: str, **kwargs) -> Product:
        product_to_update = prepare_document_to_db(
            kwargs, skip_created_at=True
        )
        query = (
            update(ProductModel)
            .where(ProductModel.id == id)
            .values(**product_to_update)
            .returning(ProductModel)
        )
        result = self.session.execute(query).scalar_one_or_none()
        self.session.commit()
        if result:
            return Product(**result.__dict__)
        return None
