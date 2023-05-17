import typing as tp
from abc import ABC, abstractmethod

from app.db import db_connection
from film.dto import FilmsDTO, FilmDTO, GenresDTO, ProductionCountriesDTO
from film.crud import queries


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
    async def find_by_id(self, film_id: int) -> FilmDTO:
        ...

    @abstractmethod
    async def find_by_title(self, title: str) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_all_genres(self) -> GenresDTO:
        ...

    @abstractmethod
    async def get_all_production_countries(self) -> ProductionCountriesDTO:
        ...

    @abstractmethod
    async def create(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def update(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def delete(self, film_id: int) -> None:
        ...

    @abstractmethod
    async def update_poster_url(self, film_id: int, poster_url: str) -> None:
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
        return FilmDTO(**film)

    async def find_by_title(self, title: str):
        films = await db_connection.fetch_all(
            queries.SEARCH_FILMS_BY_TITLE, title=f"%{title.lower()}%"
        )

        return FilmsDTO(films=films)

    async def get_all_genres(self):
        genres = await db_connection.fetch_all(queries.GET_ALL_GENRES)
        return GenresDTO(genres=genres)

    async def get_all_production_countries(self):
        production_countries = await db_connection.fetch_all(
            queries.GET_ALL_PRODUCTION_COUNTRIES
        )

        return ProductionCountriesDTO(production_countries=production_countries)

    async def update_poster_url(self, film_id: int, poster_url: str):
        await db_connection.execute_query(
            queries.UPDATE_POSTER_URL, film_id=film_id, poster_url=poster_url
        )

    async def create(self, **kwargs: ...):
        ...

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, film_id: int):
        ...
