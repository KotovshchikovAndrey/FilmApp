import typing as tp
from abc import ABC, abstractmethod

from app.db import db_connection
from film.crud import queries
from film.dto import (
    CreateFilmDTO,
    FilmDTO,
    FilmPrimaryKeyDTO,
    FilmRatingDTO,
    FilmsDTO,
    GenreDTO,
    ProductionCountryDTO,
    UpdateFilmDTO,
)


class IFilmReporitory(ABC):
    @abstractmethod
    async def get_many(
        self,
        limit: int,
        offset: int,
        genre: tp.Optional[str] = None,
        country: tp.Optional[str] = None,
    ) -> FilmsDTO:
        ...

    @abstractmethod
    async def find_by_id(self, film_id: int) -> tp.Optional[FilmDTO]:
        ...

    @abstractmethod
    async def find_by_title(self, title: str) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_all_genres(self) -> tp.List[GenreDTO]:
        ...

    @abstractmethod
    async def get_all_production_countries(self) -> tp.List[ProductionCountryDTO]:
        ...

    @abstractmethod
    async def create(self, film_create: CreateFilmDTO) -> FilmPrimaryKeyDTO:
        ...

    @abstractmethod
    async def update(
        self, film_id: int, film_update: UpdateFilmDTO
    ) -> tp.Optional[FilmPrimaryKeyDTO]:
        ...

    @abstractmethod
    async def delete(self, film_id: int) -> tp.Optional[FilmPrimaryKeyDTO]:
        ...

    @abstractmethod
    async def get_favorite_films(self, target_id: int, order_by: str) -> FilmsDTO:
        ...

    @abstractmethod
    async def aggregate_rating(self, film_id: int) -> FilmRatingDTO:
        ...

    @abstractmethod
    async def set_rating(self, user_id: int, film_id: int, value: int) -> None:
        ...


class FilmPostgresRepository(IFilmReporitory):
    async def get_many(
        self,
        limit: int,
        offset: int,
        genre: tp.Optional[str] = None,
        country: tp.Optional[str] = None,
    ):
        params = {"limit": limit, "offset": offset}
        query = queries.GET_MANY_FILMS
        if any((genre is not None, country is not None)):
            conditions = []
            query = queries.FILTER_FILMS_BY_CONDITIONS
            if genre is not None:
                conditions.append(" genre ->> 'name' = :genre ")
                params["genre"] = genre
            if country is not None:
                conditions.append(" country ->> 'iso_3166_1' = :country ")
                params["country"] = country

            query += "AND".join(conditions) + "OFFSET :offset LIMIT :limit;"

        films = await db_connection.fetch_all(query, **params)
        return FilmsDTO(films=films)

    async def find_by_id(self, film_id: int):
        film = await db_connection.fetch_one(queries.GET_FILM_BY_ID, id=film_id)
        if film is not None:
            return FilmDTO(**film)

    async def find_by_title(self, title: str):
        films = await db_connection.fetch_all(
            queries.SEARCH_FILMS_BY_TITLE, title=f"%{title.lower()}%"
        )

        return FilmsDTO(films=films)

    async def get_all_genres(self):
        genres = await db_connection.fetch_all(queries.GET_ALL_GENRES)
        return [GenreDTO(**genre) for genre in genres]

    async def get_all_production_countries(self):
        production_countries = await db_connection.fetch_all(
            queries.GET_ALL_PRODUCTION_COUNTRIES
        )

        return [
            ProductionCountryDTO(**production_country)
            for production_country in production_countries
        ]

    async def create(self, film_create: CreateFilmDTO):
        created_film = await db_connection.fetch_one(
            queries.CREATE_NEW_FILM, **film_create.dict()
        )

        return FilmPrimaryKeyDTO(**created_film)

    async def update(self, film_id: int, film_update: UpdateFilmDTO):
        updated_film = await db_connection.fetch_one(
            queries.UPDATE_FILM, film_id=film_id, **film_update.dict()
        )

        if updated_film is not None:
            return FilmPrimaryKeyDTO(**updated_film)

    async def delete(self, film_id: int):
        deleted_film = await db_connection.fetch_one(
            queries.DELETE_FILM_BY_ID, film_id=film_id
        )

        if deleted_film is not None:
            return FilmPrimaryKeyDTO(**deleted_film)

    async def get_favorite_films(self, target_id: int, order_by: str):
        films = await db_connection.fetch_all(
            queries.GET_USER_FAVORITE_FILMS + order_by, user_id=target_id
        )

        return FilmsDTO(films=films)

    async def aggregate_rating(self, film_id: int):
        rating = await db_connection.fetch_one(
            queries.AGGREGATE_AVG_FILM_RATING, film_id=film_id
        )

        return FilmRatingDTO(**rating)

    async def set_rating(self, user_id: int, film_id: int, value: int):
        return await db_connection.execute_query(
            queries.SET_FILM_RATING,
            user_id=user_id,
            film_id=film_id,
            value=value,
        )
