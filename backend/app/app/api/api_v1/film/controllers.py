import typing as tp

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint

from app.core.ioc import container, film_services
from film.dto import GetFilmsDTO

IFilmService = film_services.IFilmService


class Film(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetFilmsDTO(**request.query_params)
        films = await self.__service.get_films_assortment(dto)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=films.dict(),
        )

    async def post(self, request: Request):
        ...


class FilmDetail(HTTPEndpoint):
    async def get(self, request: Request):
        ...

    @requires("admin", status_code=status.HTTP_403_FORBIDDEN)
    async def update(self, request: Request):
        ...

    @requires("admin", status_code=status.HTTP_403_FORBIDDEN)
    async def delete(self, request: Request):
        ...


class FilmSearch(HTTPEndpoint):
    async def get(self, request: Request):
        ...
