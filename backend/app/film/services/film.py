import typing as tp
from abc import ABC, abstractmethod


class IFilmService(ABC):
    __repository: ...

    @abstractmethod
    async def get_films_assortment(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def get_film_info(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def create_new_film(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def update_film_info(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def delete_film(self, dto: ...) -> None:
        ...


class FilmService(IFilmService):
    def __init__(self, repository: ...):
        ...

    async def get_films_assortment(self, dto: ...):
        ...

    async def get_film_info(self, dto: ...):
        ...

    async def create_new_film(self, dto: ...):
        ...

    async def update_film_info(self, dto: ...):
        ...

    async def delete_film(self, dto: ...):
        ...
