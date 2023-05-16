import typing as tp

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint

from app.core.ioc import container, film_services
from film.dto import GetFilmsDTO, GetFilmDTO, SearchFilmDTO

IFilmService = film_services.IFilmService


class Film(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetFilmsDTO(**request.query_params)
        films = await self.__service.get_films_assortment(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())


class FilmDetail(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetFilmDTO(**request.path_params)
        film = await self.__service.get_film_info(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=film.dict())


class FilmFilter(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        filters = await self.__service.get_film_filters()
        return JSONResponse(status_code=status.HTTP_200_OK, content=filters.dict())


class FilmSearch(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = SearchFilmDTO(**request.query_params)
        films = await self.__service.search_film(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())
