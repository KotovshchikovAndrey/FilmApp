import typing as tp
from abc import ABC, abstractmethod

from app.exceptions.api import ApiError
from film.crud.reporitories import IFilmReporitory
from film.dto import (
    GetFilmsDTO,
    FilmsDTO,
    GetFilmDTO,
    FilmDTO,
    FilmFiltersDTO,
    SearchFilmDTO,
)


class IFilmService(ABC):
    __repository: IFilmReporitory

    @abstractmethod
    async def get_films_assortment(self, dto: GetFilmsDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_info(self, dto: GetFilmDTO) -> FilmDTO:
        ...

    @abstractmethod
    async def search_film(self, dto: SearchFilmDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_filters(self) -> FilmFiltersDTO:
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
        films = await self.__repository.get_many(
            limit=dto.limit,
            offset=dto.offset,
            genre=dto.genre,
            country=dto.country,
        )

        return films

    async def get_film_info(self, dto: GetFilmDTO):
        film = await self.__repository.find_by_id(film_id=dto.film_id)
        return film

    async def get_film_filters(self) -> FilmFiltersDTO:
        film_genres = await self.__repository.get_all_genres()
        film_countries = await self.__repository.get_all_production_countries()

        return FilmFiltersDTO(
            genres=film_genres.genres,
            countries=film_countries.production_countries,
        )

    async def search_film(self, dto: SearchFilmDTO):
        films = await self.__repository.find_by_title(title=dto.title)
        return films

    async def create_new_film(self, dto: ...):
        ...

    async def update_film_info(self, dto: ...):
        ...

    async def delete_film(self, dto: ...):
        ...
