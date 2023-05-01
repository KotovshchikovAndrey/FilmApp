import typing as tp
from abc import ABC, abstractmethod

from app.db import db_connection
from film.crud import queries


class IFilmReporitory(ABC):
    @abstractmethod
    async def get_many(self, limit: int, offset: int) -> tp.Iterable[tp.Mapping]:
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
        films = await db_connection.fetch_all(
            queries.GET_MANY_FILMS,
            limit=limit,
            offset=offset,
        )

        return films

    async def create(self, **kwargs: ...):
        ...

    async def find_by_id(self, email: str):
        ...

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int):
        ...
