from core.domain.models.product import Product
from core.domain.ports.repositories.product import ProductsRepositoryInterface


class ProductService:
    def __init__(self, repository: ProductsRepositoryInterface):
        self.repository = repository

    def register_product(self, product: Product) -> Product:
        new_product = self.repository.add(product)

        return new_product
