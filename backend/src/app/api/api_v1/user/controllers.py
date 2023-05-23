import typing as tp

from starlette.requests import Request
from starlette.responses import Response
from starlette import status
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from user.dto import ManageFavoriteFilmDTO, UpdateProfileDTO, FileDTO
from app.core.ioc import container, film_services, user_services
from app.exceptions.api import ApiError

IFilmService = film_services.IFilmService
IUserService = user_services.IUserService


class MyFavorite(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        result = await self.__service.get_favorites(request.user.instance.id)
        return JSONResponse(content=result.dict()["films"])

    @requires("authenticated", status_code=401)
    @requires("active", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.user.instance.id, **data)
        await self.__service.add_to_favorite(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    @requires("active", status_code=403)
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
        await self.__service.find_user_by_id(
            request.path_params["user_id"]
        )  # Если пользователь не существует, будет ошибка
        result = await self.__service.get_favorites(request.path_params["user_id"])
        return JSONResponse(content=result.dict()["films"])

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.path_params["user_id"], **data)
        await self.__service.find_user_by_id(
            dto.user_id
        )  # Если пользователь не существует, будет ошибка
        await self.__service.add_to_favorite(dto)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.path_params["user_id"], **data)
        await self.__service.find_user_by_id(
            dto.user_id
        )  # Если пользователь не существует, будет ошибка
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
    async def put(self, request: Request):
        user = request.user.instance
        data = await request.json()

        dto = UpdateProfileDTO(**data)
        await self.__service.update_user_profile(user=user, dto=dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

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


class ProfileAvatar(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def put(self, request: Request):
        user = request.user.instance
        async with request.form() as form:
            avatar = form.get("avatar", None)
            if avatar is None:
                raise ApiError.bad_request(message="Avatar file was not sent!")

            avatar_filename = avatar.filename
            avatar_file = await avatar.read()
            avatar = FileDTO(filename=avatar_filename, content=avatar_file)

        user_avatar = await self.__service.set_user_avatar(user=user, dto=avatar)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=user_avatar.dict(),
        )


class BanUser(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def put(self, request: Request):
        await self.__service.ban_user(request.path_params["user_id"])
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class UnbanUser(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def put(self, request: Request):
        await self.__service.unban_user(request.path_params["user_id"])
        return Response(status_code=status.HTTP_204_NO_CONTENT)
