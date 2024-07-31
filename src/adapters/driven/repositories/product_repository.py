from config.database import get_mongo_database
from core.domain.models.product import Product
from core.domain.ports.repositories.product import ProductsRepositoryInterface


class ProductMongoRepository(ProductsRepositoryInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Products"]

    def _add(self, product: Product) -> None:
        self.collection.insert_one(product.model_dump())

    def _get_by_id(self, id: int) -> Product | None:
        query = self.get_product_by_id_query(id=id)
        product = self.collection.find_one(query)
        if product:
            return Product(**product)
        return None

    def _list_products(self) -> list[Product] | None:
        query = self.get_list_product_query()
        products = self.collection.find(query)
        if products:
            return [Product(**product) for product in products]
        return None

    @staticmethod
    def get_product_by_id_query(id: int) -> dict:
        query = {"id": id}
        return query

    @staticmethod
    def get_list_product_query() -> dict:
        query = {}
        return query
