import typing as tp
from abc import ABC, abstractmethod

from film.crud.reporitories import IFilmReporitory
from film.dto import GetFilmsDTO, FilmsDTO, GetFilmDTO, FilmDTO


class IFilmService(ABC):
    __repository: IFilmReporitory

    @abstractmethod
    async def get_films_assortment(self, dto: GetFilmsDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_info(self, dto: GetFilmDTO) -> FilmDTO:
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
    def __init__(self, repository: IFilmReporitory):
        self.__repository = repository

    async def get_films_assortment(self, dto: GetFilmsDTO):
        films = await self.__repository.get_many(limit=dto.limit, offset=dto.offset)
        return FilmsDTO(films=films)

    async def get_film_info(self, dto: GetFilmDTO):
        film = await self.__repository.find_by_id(film_id=dto.film_id)
        return FilmDTO(**film)

    async def create_new_film(self, dto: ...):
        ...

    async def update_film_info(self, dto: ...):
        ...

    async def delete_film(self, dto: ...):
        ...
