import typing as tp

from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from app.core.ioc import container, film_services, user_services

IFilmService = film_services.IFilmService
IUserService = user_services.IUserService


class MyFavorite(HTTPEndpoint):
    __film_service: IFilmService = container.resolve(IFilmService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        result = await self.__film_service.get_user_favorite_films(target_id=request.user.instance.id)
        return JSONResponse(
            content=result.dict()["films"]
        )

    @requires("authenticated", status_code=401)
    async def post(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        ...


class UserFavorite(HTTPEndpoint):
    __film_service: IFilmService = container.resolve(IFilmService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        result = await self.__film_service.get_user_favorite_films(target_id=request.path_params["user_id"])
        return JSONResponse(
            content=result.dict()["films"]
        )

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def post(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        ...


# Profiles
class MyProfile(HTTPEndpoint):
    __film_service: IFilmService = container.resolve(IFilmService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        user = request.user.instance
        films = await self.__film_service.get_user_favorite_films(target_id=user.id)
        return JSONResponse(
            content=user.dict() | films.dict()
        )

    @requires("authenticated", status_code=401)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        ...


class Profile(HTTPEndpoint):
    __film_service: IFilmService = container.resolve(IFilmService)
    __user_service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        user = await self.__user_service.find_user_by_id(request.path_params["user_id"])
        films = await self.__film_service.get_user_favorite_films(target_id=user.id)
        return JSONResponse(
            content=user.dict() | films.dict()
        )

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        ...
