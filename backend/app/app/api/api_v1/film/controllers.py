import typing as tp

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.endpoints import HTTPEndpoint

from film.services.imdb import fetch_poster_url_by_imdb_id
from app.core.ioc import container, film_services
from film.dto import (
    GetFilmsDTO,
    GetFilmDTO,
    SearchFilmDTO,
    CreateFilmDTO,
    UpdateFilmDTO,
)

IFilmService = film_services.IFilmService


# class Test(HTTPEndpoint):
#     async def get(self, request: Request):
#         poster_url = await fetch_poster_url_by_imdb_id(imdb_id="tt0022151")
#         # return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "OK"})
#         return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": poster_url})


class Film(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetFilmsDTO(**request.query_params)
        films = await self.__service.get_films_assortment(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())

    # Нужно ограничить доступ (доступно только админам)
    async def post(self, request: Request):
        data = await request.json()
        dto = CreateFilmDTO(**data)
        created_film = await self.__service.create_new_film(dto)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_film)


class FilmDetail(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetFilmDTO(**request.path_params)
        film = await self.__service.get_film_info(dto)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=film.dict(exclude={"imdb_id"}),
        )

    # Нужно ограничить доступ (доступно только админам)
    async def put(self, request: Request):
        film_id = request.path_params["film_id"]
        data = await request.json()
        dto = UpdateFilmDTO(**data)
        updated_film = await self.__service.update_film_info(film_id, dto)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_film)

    # Нужно ограничить доступ (доступно только админам)
    async def delete(self, request: Request):
        film_id = request.path_params["film_id"]
        deleted_film = await self.__service.delete_film(film_id)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=deleted_film)


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


class Poster(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        film_id = request.path_params["film_id"]
        poster = await self.__service.get_poster_for_film(film_id)

        return Response(content=poster, media_type="image/jpeg")
