import typing as tp
import json

from pydantic import BaseModel, Json, validator
from datetime import date, datetime


class FilmPrimaryKeyDTO(BaseModel):
    id: int


class FilmBase(FilmPrimaryKeyDTO):
    title: str
    is_adult: bool
    tagline: tp.Optional[str] = None


class ProductionCompanyDTO(BaseModel):
    id: int
    name: str


class GenreDTO(BaseModel):
    id: int
    name: str


class GenresDTO(BaseModel):
    genres: tp.List[GenreDTO]

    @validator("genres")
    def validate_genres(cls, values_list: tp.List[tp.Mapping[str, str]]):
        return list(
            map(lambda value: GenreDTO(**json.loads(value["genre"])), values_list)
        )


class ProductionCountryDTO(BaseModel):
    iso_name: Json | str
    public_name: Json | str


class ProductionCountriesDTO(BaseModel):
    production_countries: tp.List[ProductionCountryDTO]


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
    genre: tp.Optional[str] = None
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
    def validate_json(cls, value: tp.List[tp.Mapping[str, str]]):
        try:
            value = json.dumps(value)
        except:
            raise ValueError(f"{value} - Невалидный json формат!")

        return value

    @validator("release_date", pre=True)
    def validate_release_date(cls, value: str):
        try:
            year, month, day = map(int, value.split("-"))
            value = date(year, month, day)
        except:
            raise ValueError("Невалидный формат даты для поля release_date!")

        return value


UpdateFilmDTO = CreateFilmDTO
