import typing as tp
import json

from pydantic import BaseModel, Json, validator
from datetime import date


class FilmBase(BaseModel):
    id: int
    title: str
    is_adult: bool
    imdb_id: tp.Optional[str] = None
    poster_url: tp.Optional[str] = None
    tagline: tp.Optional[str] = None


class ProductionCompanyDTO(BaseModel):
    id: int
    name: str


class GenreDTO(BaseModel):
    id: int
    name: str


class GenresDTO(BaseModel):
    genres: tp.List[GenreDTO]

    @validator("genres", pre=True)
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
    genres: tp.List[GenreDTO]
    production_companies: tp.Optional[tp.List[ProductionCompanyDTO]] = None
    production_countries: tp.Optional[tp.List[ProductionCountryDTO]] = None

    class Config:
        fields = {"tagline": {"exclude": True}}

    @validator("genres", pre=True)
    def validate_genres(cls, value: tp.List[tp.Mapping[str, str]]):
        genres = json.loads(value)
        return [GenreDTO(**genre) for genre in genres]

    @validator("production_countries", pre=True)
    def validate_production_countries(cls, value: tp.List[tp.Mapping[str, str]] | None):
        if value is None:
            return value

        production_countries = json.loads(value)
        return [
            ProductionCountryDTO(
                iso_name=country["iso_3166_1"],
                public_name=country["name"],
            )
            for country in production_countries
        ]

    @validator("production_companies", pre=True)
    def validate_production_companies(cls, value: tp.List[tp.Mapping[str, str]] | None):
        if value is None:
            return value

        production_companies = json.loads(value)
        return [ProductionCompanyDTO(**company) for company in production_companies]

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


class SearchFilmDTO(BaseModel):
    title: str
