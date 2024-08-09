import abc

from core.domain.models.product import Product


class ProductsRepositoryInterface(abc.ABC):
    def __init__(self): ...

    def add(self, product: Product) -> Product:
        new_product = self._add(product)
        return new_product

    def get_by_id(self, id: str) -> Product:
        product = self._get_by_id(id)
        return product

    def list_products(
        self, filter: dict, page: int, page_size: int
    ) -> list[Product]:
        products = self._list_products(
            filter=filter, page=page, page_size=page_size
        )
        return products

    def count_products(self, filter: dict) -> int:
        total_products = self._count_products(filter=filter)
        return total_products

    def delete_product(self, id: str) -> bool:
        was_product_deleted = self._delete_product(id=id)
        return was_product_deleted

    def exists_by_id(self, id: str) -> bool:
        return self._exists_by_id(id)

    @abc.abstractmethod
    def _add(self, product: Product) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: str) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_products(
        self, filter: dict, page: int, page_size: int
    ) -> list[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def _count_products(self, filter: dict) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_product(self, id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _exists_by_id(self, id: str) -> bool:
        raise NotImplementedError
