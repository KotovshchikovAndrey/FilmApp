import typing as tp

from starlette.requests import Request
from starlette.responses import Response
from starlette import status
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from user.dto import ManageFavoriteFilmDTO
from app.core.ioc import container, film_services, user_services

IFilmService = film_services.IFilmService
IUserService = user_services.IUserService


class MyFavorite(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        result = await self.__service.get_favorites(request.user.instance.id)
        return JSONResponse(content=result.dict()["films"])

    @requires("authenticated", status_code=401)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.user.instance.id, **data)
        await self.__service.add_to_favorite(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.user.instance.id, **data)
        await self.__service.delete_from_favorite(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


class UserFavorite(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        await self.__service.get_current_user(request.path_params["user_id"])  # Если пользователь не существует, будет ошибка
        result = await self.__service.get_favorites(request.path_params["user_id"])
        return JSONResponse(content=result.dict()["films"])

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.path_params["user_id"], **data)
        await self.__service.get_current_user(dto.user_id)  # Если пользователь не существует, будет ошибка
        await self.__service.add_to_favorite(dto)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.path_params["user_id"], **data)
        await self.__service.get_current_user(dto.user_id)  # Если пользователь не существует, будет ошибка
        await self.__service.delete_from_favorite(dto)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


# Profiles
class MyProfile(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        user = request.user.instance
        films = await self.__service.get_favorites(user.id)
        return JSONResponse(content=user.dict() | films.dict())

    @requires("authenticated", status_code=401)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        ...


class Profile(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        user = await self.__service.find_user_by_id(request.path_params["user_id"])
        films = await self.__service.get_favorites(user.id)
        return JSONResponse(content=user.dict() | films.dict())

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        ...
