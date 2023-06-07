import typing as tp

import json
from datetime import date
from pydantic import BaseModel, validator

from user.dto import UserBase


class FilmPrimaryKeyDTO(BaseModel):
    id: int


class FilmBase(FilmPrimaryKeyDTO):
    title: str
    is_adult: bool
    tagline: tp.Optional[str] = None


class ProductionCompanyDTO(BaseModel):
    id: tp.Optional[int] = None
    name: str


class GenreDTO(BaseModel):
    id: tp.Optional[int] = None
    name: str


class ProductionCountryDTO(BaseModel):
    name: str
    iso_3166_1: str


class FilmFiltersDTO(BaseModel):
    genres: tp.List[GenreDTO]
    countries: tp.List[ProductionCountryDTO]


class FilmDTO(FilmBase):
    description: tp.Optional[str] = None
    imdb_id: tp.Optional[str] = None
    language: tp.Optional[str] = None
    budget: int
    release_date: str
    time: tp.Optional[float] = None
    genres: tp.List[tp.Mapping[str, str]]
    production_companies: tp.Optional[tp.List[tp.Mapping[str, str]]] = None
    production_countries: tp.Optional[tp.List[tp.Mapping[str, str]]] = None

    class Config:
        fields = {"tagline": {"exclude": True}}

    @validator("genres", "production_companies", "production_countries", pre=True)
    def validate_json(cls, value: tp.List[tp.Mapping[str, str]] | None):
        if value is not None:
            return json.loads(value)

    @validator("release_date", pre=True)
    def validate_release_date(cls, value: date):
        return str(value)


class GetFilmsDTO(BaseModel):
    limit: int
    offset: int = 0
    genre: tp.Optional[int] = None
    country: tp.Optional[str] = None


class FilmsDTO(BaseModel):
    films: tp.List[FilmBase]


class GetFilmDTO(BaseModel):
    film_id: int


class GetPosterDTO(BaseModel):
    film_id: int
    size: tp.Optional[int] = None

    @validator("size")
    def validate_size(cls, value: int | None):
        poster_sizes = {200, 300, 500}
        if value not in poster_sizes:
            raise ValueError(
                f"Недопустимый размер постера! Допустимые размеры {poster_sizes}"
            )

        return value


class SearchFilmDTO(BaseModel):
    title: str


class FilmTrailerDTO(BaseModel):
    key: str
    site: str


class CreateFilmDTO(BaseModel):
    title: str
    is_adult: bool
    tagline: tp.Optional[str] = None
    description: tp.Optional[str] = None
    imdb_id: tp.Optional[str] = None
    language: tp.Optional[str] = None
    budget: int
    release_date: date
    time: tp.Optional[float] = None
    genres: str
    production_companies: tp.Optional[str] = None
    production_countries: tp.Optional[str] = None

    @validator("genres", "production_companies", "production_countries", pre=True)
    def validate_json(cls, value: tp.Any):
        """Проверяем, можно ли введенные данные преобразовать в json формат"""

        try:
            value = json.dumps(value)
        except Exception:
            raise ValueError(f"{value} - Invalid json format!")

        return value

    @validator("genres")
    def validate_genres(cls, value: str):
        """Проверяем, что json поле genres содержит все необходимые поля"""

        genres = json.loads(value)
        if not isinstance(genres, list):  # проверяем, что нам пришел именно список
            raise ValueError(f"Field genres must be iterable!")

        for genre in genres:
            GenreDTO(**genre)  # если встретит невалидные данные, выплюнит ошибку

        return value

    @validator("production_countries")
    def validate_production_countries(cls, value: str | None):
        """Проверяем, что json поле production_countries содержит все необходимые поля"""

        production_countries = json.loads(value)
        if production_countries is None:  # вернет None, если в json null
            return

        if not isinstance(
            production_countries, list
        ):  # проверяем, что нам пришел именно список
            raise ValueError(f"Field production_countries must be iterable!")

        for country in production_countries:
            ProductionCountryDTO(
                **country
            )  # если встретит невалидные данные, выплюнит ошибку

        return value

    @validator("production_companies")
    def validate_production_companies(cls, value: str):
        """Проверяем, что json поле production_companies содержит все необходимые поля"""

        production_companies = json.loads(value)
        if production_companies is None:  # вернет None, если в json null
            return

        if not isinstance(
            production_companies, list
        ):  # проверяем, что нам пришел именно список
            raise ValueError(f"Field production_companies must be iterable!")

        for company in production_companies:
            ProductionCompanyDTO(
                **company
            )  # если встретит невалидные данные, выплюнит ошибку

        return value

    @validator("release_date", pre=True)
    def validate_release_date(cls, value: str | date):
        if isinstance(value, date):
            return value

        try:
            year, month, day = map(int, value.split("-"))
            value = date(year, month, day)
        except Exception:
            raise ValueError("Invalid date format for release_date!")

        return value

    @validator("title")
    def validate_title(cls, value: str):
        if not (0 < len(value) <= 255):
            raise ValueError("The title field must be between 0 and 255 characters!")

        return value

    @validator("time")
    def validate_time(cls, value: float | None):
        if (value is not None) and (value <= 0):
            raise ValueError("The time field must be greater 0!")

        return value


class UpdateFilmDTO(CreateFilmDTO):
    __annotations__ = {
        k: tp.Optional[v] for k, v in CreateFilmDTO.__annotations__.items()
    }


class SetFilmRatingDTO(BaseModel):
    user: UserBase
    film_id: int
    value: int

    @validator("value")
    def validate_value(cls, value: int):
        if not (0 <= value <= 9):
            raise ValueError("Rating value must be between 0 and 9!")

        return value


class ResetFilmRaitingDTO(BaseModel):
    user: UserBase
    film_id: int


class FilmRatingDTO(BaseModel):
    film_id: int
    rating: float
