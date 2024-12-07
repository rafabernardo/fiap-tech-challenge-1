from core.exceptions.commons_exceptions import NoDocumentsFoundException
from db.interfaces.product import ProductsRepositoryInterface
from models.product import Product


class ProductService:
    def __init__(self, repository: ProductsRepositoryInterface):
        self.repository = repository

    def register_product(self, product: Product) -> Product:
        new_product = self.repository.add(product)

        return new_product

    def list_products(
        self, filter: dict, page: int, page_size: int
    ) -> list[Product]:
        paginated_orders = self.repository.list_products(
            filter=filter, page=page, page_size=page_size
        )
        return paginated_orders

    def get_product_by_id(self, id: int) -> Product | None:
        product = self.repository.get_by_id(id)
        return product

    def count_products(self, filter: dict) -> int:
        total_products = self.repository.count_products(filter=filter)
        return total_products

    def delete_product(self, id: int) -> bool:
        product_exists = self.repository.exists_by_id(id)
        if not product_exists:
            raise NoDocumentsFoundException()

        return self.repository.delete_product(id)

    def update_product(self, id: int, **kwargs) -> Product:
        product = self.repository._exists_by_id(id)
        if not product:
            raise NoDocumentsFoundException()
        return self.repository.update_product(id, **kwargs)
