from bson import ObjectId

from db.interfaces.product import ProductsRepositoryInterface
from db.mongodb.database import get_mongo_database
from models.product import Product
from repositories.utils import prepare_document_to_db, replace_id_key


class ProductMongoRepository(ProductsRepositoryInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Products"]

    def _add(self, product: Product) -> Product:
        product_data = product.model_dump()
        product_to_db = prepare_document_to_db(product_data)
        self.collection.insert_one(product_to_db)

        final_product = replace_id_key(product_to_db)
        return Product(**final_product)

    def _get_by_id(self, id: str) -> Product | None:
        query = self.get_product_by_id_query(id=id)
        product = self.collection.find_one(query)
        if product:
            final_product = replace_id_key(product)
            return Product(**final_product)
        return None

    def _list_products(
        self, filter: dict, page: int, page_size: int
    ) -> list[Product]:
        skip = (page - 1) * page_size
        products = list(
            self.collection.find(filter).skip(skip).limit(page_size)
        )
        return [Product(**replace_id_key(product)) for product in products]

    def _count_products(self, filter: dict) -> int:
        return self.collection.count_documents(filter)

    def _exists_by_id(self, id: str) -> bool:
        query = self.get_product_by_id_query(id=id)
        return self.collection.count_documents(query) > 0

    def _delete_product(self, id: str) -> bool:
        query = self.get_product_by_id_query(id=id)
        result = self.collection.delete_one(query)
        was_user_deleted = result.deleted_count > 0
        return was_user_deleted

    def _update_product(self, id: str, **kwargs) -> Product:
        id_filter = self.get_product_by_id_query(id=id)
        product_to_update = prepare_document_to_db(
            kwargs, skip_created_at=True
        )
        query = self.get_product_update_data(product_to_update)
        updated_product = self.collection.find_one_and_update(
            id_filter,
            query,
            return_document=True,
        )

        final_product = replace_id_key(updated_product)
        return final_product

    @staticmethod
    def get_product_by_id_query(id: str) -> dict:
        query = {"_id": ObjectId(id)}
        return query

    @staticmethod
    def get_list_product_query() -> dict:
        query = {}
        return query

    @staticmethod
    def get_product_update_data(kwargs: dict) -> dict:
        update_data = {"$set": kwargs}
        return update_data
