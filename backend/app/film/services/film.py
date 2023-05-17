import typing as tp
from abc import ABC, abstractmethod

import asyncio
from app.core import config
from app.exceptions.api import ApiError
from film.crud.reporitories import IFilmReporitory
from film.dto import (
    GetFilmsDTO,
    FilmsDTO,
    FilmBase,
    GetFilmDTO,
    FilmDTO,
    FilmFiltersDTO,
    SearchFilmDTO,
)

from film.services.imdb import fetch_poster_url_by_imdb_id
from film.utils.file_uploader import FileUploader


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

        async_tasks = []
        for film in films.films:
            if film.poster_url is None:
                async_tasks.append(self.__set_poster_url_for_film(film))

        await asyncio.gather(*async_tasks)
        return films

    async def get_film_info(self, dto: GetFilmDTO):
        film = await self.__repository.find_by_id(film_id=dto.film_id)
        if film.poster_url is not None:
            return film

        await self.__set_poster_url_for_film(film)
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

    async def __set_poster_url_for_film(self, dto: FilmBase):
        if dto.imdb_id is None:
            return dto

        poster_url = await fetch_poster_url_by_imdb_id(dto.imdb_id)
        if poster_url is not None:
            file_uloader = FileUploader(upload_dir=config.UPLOAD_DIR + "/posters")
            uploaded_file_name = await file_uloader.upload(
                file_url=poster_url, file_name=f"poster_{dto.id}"
            )

            await self.__repository.update_poster_url(dto.id, uploaded_file_name)
            dto.poster_url = f"/{uploaded_file_name}"

        return dto
