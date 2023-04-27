import typing as tp
from abc import ABC, abstractmethod


class IFilmReporitory(ABC):
    @abstractmethod
    async def get_many(self, limit: int, offset: int) -> ...:
        ...

    @abstractmethod
    async def create(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def find_by_id(self, email: str) -> ...:
        ...

    @abstractmethod
    async def update(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...


class FilmPostgresRepository(IFilmReporitory):
    async def get_many(self, limit: int, offset: int):
        ...

    async def create(self, **kwargs: ...):
        ...

    async def find_by_id(self, email: str):
        ...

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int):
        ...
