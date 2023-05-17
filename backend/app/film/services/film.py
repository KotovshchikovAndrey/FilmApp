import typing as tp
from abc import ABC, abstractmethod

import asyncio
from app.core import config
from app.exceptions.api import ApiError
from film.crud.reporitories import IFilmReporitory
from film.dto import (
    FilmPrimaryKeyDTO,
    GetFilmsDTO,
    FilmsDTO,
    CreateFilmDTO,
    UpdateFilmDTO,
    GetFilmDTO,
    FilmDTO,
    FilmFiltersDTO,
    SearchFilmDTO,
)

from film.services.imdb import fetch_poster_url_by_imdb_id, fetch_poster_binary_file
from app.utils.file_manager import FileManager


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
    async def get_poster_for_film(self, film_id: int) -> bytes:
        ...

    @abstractmethod
    async def create_new_film(self, dto: CreateFilmDTO) -> int:
        ...

    @abstractmethod
    async def update_film_info(
        self, film_id: int, dto: UpdateFilmDTO
    ) -> tp.Optional[int]:
        ...

    @abstractmethod
    async def delete_film(self, film_id: int) -> tp.Optional[int]:
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

    async def get_poster_for_film(self, film_id: int):
        film = await self.__repository.find_by_id(film_id)
        if film is None:
            raise ApiError.not_found(message="Фильм с таким id не найден!")

        imdb_id = film.imdb_id
        if imdb_id is not None:
            poster_url = await fetch_poster_url_by_imdb_id(imdb_id)
            if poster_url is not None:
                poster = await fetch_poster_binary_file(poster_url)
                return poster

        file_manager = FileManager(upload_dir=config.UPLOAD_DIR + "/posters")
        poster = await file_manager.read("default_poster.jpg")

        return poster

    async def search_film(self, dto: SearchFilmDTO):
        films = await self.__repository.find_by_title(title=dto.title)
        return films

    async def create_new_film(self, dto: CreateFilmDTO):
        created_film = await self.__repository.create(dto)
        return created_film.id

    async def update_film_info(self, film_id: int, dto: UpdateFilmDTO):
        updated_film = await self.__repository.update(film_id, dto)
        if updated_film is not None:
            return updated_film.id

    async def delete_film(self, film_id: int):
        deleted_film = await self.__repository.delete(film_id)
        if deleted_film is not None:
            return deleted_film.id
