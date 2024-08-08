from core.domain.models.product import Product
from core.domain.ports.repositories.product import ProductsRepositoryInterface


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

    def count_products(self, filter: dict) -> int:
        total_products = self.repository.count_products(filter=filter)
        return total_products
