import abc

from core.domain.models.product import Product


class ProductsRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen: set[Product] = set()

    def add(self, product: Product) -> None:
        self._add(product)
        self.seen.add(product)

    def get_by_id(self, id: int) -> Product:
        product = self._get_by_id(id)
        if product:
            self.seen.add(product)
        return product

    def list_products(self) -> list[Product]:
        products = self._list_products()
        if products:
            self.seen.union(set(products))
        return products

    @abc.abstractmethod
    def _add(self, product: Product) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: int) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_products(self) -> list[Product]:
        raise NotImplementedError