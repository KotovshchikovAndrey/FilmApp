import typing as tp

from starlette import status
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.endpoints import HTTPEndpoint

from app.core.ioc import container, film_services
from film.dto import (
    GetFilmsDTO,
    SearchFilmDTO,
    CreateFilmDTO,
    UpdateFilmDTO,
    GetPosterDTO,
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

    @requires("admin", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = CreateFilmDTO(**data)
        created_film = await self.__service.create_new_film(dto)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_film)


class FilmDetail(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        film_id = request.path_params["film_id"]
        film = await self.__service.get_film_info(film_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=film.dict(exclude={"imdb_id"}),
        )

    @requires("admin", status_code=403)
    async def put(self, request: Request):
        film_id = request.path_params["film_id"]
        data = await request.json()
        dto = UpdateFilmDTO(**data)
        updated_film = await self.__service.update_film_info(film_id, dto)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_film)

    @requires("admin", status_code=403)
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
        dto = GetPosterDTO(**request.query_params, **request.path_params)
        poster = await self.__service.get_poster_for_film(dto)

        return Response(content=poster, media_type="image/jpeg")


class Trailer(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        film_id = request.path_params["film_id"]
        trailer = await self.__service.get_trailer_for_film(film_id)

        return JSONResponse(status_code=status.HTTP_200_OK, content=trailer.dict())
