import typing as tp
from pydantic import BaseModel, Json
from datetime import date


class FilmBase(BaseModel):
    id: int
    title: str
    is_adult: bool


class FilmDTO(FilmBase):
    release_date: date
    time: float
    budget: int
    genres: tp.List[Json[tp.Any]]
    production_companies: Json[tp.Any]
    production_countries: Json[tp.Any]
    description: tp.Optional[str] = None
    poster_path: tp.Optional[str] = None
    imdb_id: tp.Optional[str] = None
    language: tp.Optional[str] = None


class GetFilmsDTO(BaseModel):
    limit: int
    offset: int = 0


class FilmsDTO(BaseModel):
    films: tp.List[FilmBase]


class GetFilmDTO(BaseModel):
    film_id: int
