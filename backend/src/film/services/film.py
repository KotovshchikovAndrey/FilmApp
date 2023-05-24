import typing as tp
from abc import ABC, abstractmethod

from app.core import config
from app.exceptions.api import ApiError
from film.crud.reporitories import IFilmReporitory
from film.services import imdb
from app.utils.file_manager import FileManager

from film.dto import (
    GetFilmsDTO,
    FilmsDTO,
    CreateFilmDTO,
    UpdateFilmDTO,
    FilmDTO,
    FilmFiltersDTO,
    SearchFilmDTO,
    GetPosterDTO,
    FilmTrailerDTO,
    FilmRaitingDTO,
    SetFilmRaitingDTO,
)


class IFilmService(ABC):
    __repository: IFilmReporitory

    @abstractmethod
    async def get_films_assortment(self, dto: GetFilmsDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_info(self, film_id: int) -> FilmDTO:
        ...

    @abstractmethod
    async def search_film(self, dto: SearchFilmDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_filters(self) -> FilmFiltersDTO:
        ...

    @abstractmethod
    async def get_poster_for_film(self, dto: GetPosterDTO) -> bytes:
        ...

    @abstractmethod
    async def get_trailer_for_film(self, film_id: int) -> FilmTrailerDTO:
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

    @abstractmethod
    async def get_user_favorite_films(self, target_id: int, order_by: str) -> FilmsDTO:
        ...

    @abstractmethod
    async def calculate_film_raiting(self, film_id: int) -> FilmRaitingDTO:
        ...

    @abstractmethod
    async def set_film_raiting(self, dto: SetFilmRaitingDTO) -> None:
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

    async def get_film_info(self, film_id: int):
        film = await self.__repository.find_by_id(film_id)
        if film is None:
            raise ApiError.not_found(message="Film not found!")

        return film

    async def get_film_filters(self) -> FilmFiltersDTO:
        film_genres = await self.__repository.get_all_genres()
        film_countries = await self.__repository.get_all_production_countries()

        return FilmFiltersDTO(
            genres=film_genres.genres,
            countries=film_countries.production_countries,
        )

    async def get_poster_for_film(self, dto: GetPosterDTO):
        film = await self.__repository.find_by_id(dto.film_id)
        if film is None:
            raise ApiError.not_found(message="Film not found!")

        imdb_id = film.imdb_id
        if imdb_id is not None:
            poster_url = await imdb.fetch_poster_url_by_imdb_id(imdb_id)
            if poster_url is not None:
                poster = await imdb.fetch_poster_binary_file(poster_url, dto.size)
                return poster

        file_manager = FileManager(upload_dir=config.UPLOAD_DIR + "/posters")
        poster = await file_manager.read("default_poster.jpg")

        return poster

    async def get_trailer_for_film(self, film_id: int):
        film = await self.__repository.find_by_id(film_id)
        if film is None:
            raise ApiError.not_found(message="Film not found!")

        imdb_id = film.imdb_id
        if imdb_id is not None:
            trailer_url = await imdb.fetch_trailer_url_by_imdb_id(imdb_id)
            if trailer_url is not None:
                return trailer_url

        raise ApiError.not_found(message="Trailer not found!")

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

    async def get_user_favorite_films(self, target_id: int, order_by: str):
        films = await self.__repository.get_favorite_films(target_id, order_by)
        return films

    async def calculate_film_raiting(self, film_id: int):
        raiting = await self.__repository.agregate_raiting(film_id)
        return raiting

    async def set_film_raiting(self, dto: SetFilmRaitingDTO):
        return await self.__repository.set_raiting(
            user_id=dto.user.id,
            film_id=dto.film_id,
            value=dto.value,
        )
