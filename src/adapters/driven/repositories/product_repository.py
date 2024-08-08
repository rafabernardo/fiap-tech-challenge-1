from adapters.driven.repositories.utils import (
    prepare_document_to_db,
    replace_id_key,
)
from config.database import get_mongo_database
from core.domain.models.product import Product
from core.domain.ports.repositories.product import ProductsRepositoryInterface


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

    def _get_by_id(self, id: int) -> Product | None:
        query = self.get_product_by_id_query(id=id)
        product = self.collection.find_one(query)
        if product:
            return Product(**product)
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

    @staticmethod
    def get_product_by_id_query(id: int) -> dict:
        query = {"id": id}
        return query

    @staticmethod
    def get_list_product_query() -> dict:
        query = {}
        return query
