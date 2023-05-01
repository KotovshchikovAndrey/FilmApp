import typing as tp
from pydantic import BaseModel


class FilmBase(BaseModel):
    id: int
    title: str
    is_adult: bool


class GetFilmsDTO(BaseModel):
    limit: int
    offset: int = 0


class FilmsDTO(BaseModel):
    films: tp.List[FilmBase]
