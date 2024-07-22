from abc import ABC, abstractmethod

from src.core.domain.models.register import Register


class BookPort(ABC):

    @abstractmethod
    async def get_books(self) -> Register | None:
        raise NotImplementedError

    @abstractmethod
    async def create_book(self, book: Register) -> Register:
        raise NotImplementedError