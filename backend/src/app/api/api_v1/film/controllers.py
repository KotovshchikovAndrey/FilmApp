import typing as tp
from loguru import logger

from starlette import status
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.ioc import container, film_services
from film.dto import (
    CreateFilmDTO,
    GetFilmsDTO,
    GetPosterDTO,
    SearchFilmDTO,
    SetFilmRatingDTO,
    UpdateFilmDTO,
    ResetFilmRaitingDTO,
    AddCommentDTO,
    UpdateCommentDTO,
)

IFilmService = film_services.IFilmService


class Test(HTTPEndpoint):
    async def get(self, request: Request):
        ...


class Film(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetFilmsDTO(**request.query_params)
        films = await self.__service.get_films_assortment(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())

    # @requires("admin", status_code=403)
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

    # @requires("admin", status_code=403)
    async def patch(self, request: Request):
        film_id = request.path_params["film_id"]
        data = await request.json()

        dto = UpdateFilmDTO(**data)
        updated_film = await self.__service.update_film_info(film_id, dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=updated_film)

    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        film_id = request.path_params["film_id"]
        deleted_film = await self.__service.delete_film(film_id)

        return JSONResponse(status_code=status.HTTP_200_OK, content=deleted_film)


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


class FilmGigaSearch(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def post(self, request: Request):
        data = await request.json()
        dto = SearchFilmDTO(**data)
        film = await self.__service.giga_search_film(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=film.dict())


class Poster(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        dto = GetPosterDTO(**request.query_params, **request.path_params)
        poster = await self.__service.get_poster_for_film(dto)

        response = Response(content=poster, media_type="image/jpeg")
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response


class Trailer(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        film_id = request.path_params["film_id"]
        trailer = await self.__service.get_trailer_for_film(film_id)

        response = JSONResponse(status_code=status.HTTP_200_OK, content=trailer.dict())
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response


class FilmRating(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        film_id = request.path_params["film_id"]
        film_rating = await self.__service.calculate_film_rating(film_id)

        return JSONResponse(status_code=status.HTTP_200_OK, content=film_rating.dict())

    @requires("authenticated", status_code=401)
    async def put(self, request: Request):
        user = request.user.instance
        film_id = request.path_params["film_id"]
        data = await request.json()

        dto = SetFilmRatingDTO(**data, film_id=film_id, user=user)
        await self.__service.set_film_rating(dto)

        logger.info(
            f"user email={user.email} ip={request.client.host} set raiting to film id={film_id}"
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        user = request.user.instance
        film_id = request.path_params["film_id"]

        dto = ResetFilmRaitingDTO(user=user, film_id=film_id)
        await self.__service.reset_film_rating(dto)

        logger.info(
            f"user email={user.email} ip={request.client.host} drop raiting to film id={film_id}"
        )

        return Response(status_code=204)


class FilmComment(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    async def get(self, request: Request):
        film_id = request.path_params["film_id"]
        film_comments = await self.__service.get_film_comments(film_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=film_comments.dict(),
        )

    @requires("authenticated", status_code=401)
    async def post(self, request: Request):
        user = request.user.instance
        film_id = request.path_params["film_id"]

        data = await request.json()
        dto = AddCommentDTO(**data, user=user, film_id=film_id)
        added_comment = await self.__service.add_comment_to_film(dto)

        logger.info(
            f"user email={user.email} ip={request.client.host} create comment to film id={film_id}"
        )

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_comment)


class FilmCommentDetail(HTTPEndpoint):
    __service: IFilmService = container.resolve(IFilmService)

    @requires("authenticated", status_code=401)
    async def patch(self, request: Request):
        user = request.user.instance
        comment_id = request.path_params["comment_id"]

        data = await request.json()
        dto = UpdateCommentDTO(**data, user=user, comment_id=comment_id)
        updated_comment = await self.__service.update_film_comment(dto)

        logger.info(
            f"user email={user.email} ip={request.client.host} update comment id={comment_id}"
        )

        return JSONResponse(status_code=status.HTTP_200_OK, content=updated_comment)

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        user = request.user.instance
        comment_id = request.path_params["comment_id"]

        deleted_comment = await self.__service.delete_film_comment(
            comment_id=comment_id, user=user
        )

        logger.info(
            f"user email={user.email} ip={request.client.host} drop comment id={comment_id}"
        )

        return JSONResponse(status_code=status.HTTP_200_OK, content=deleted_comment)
