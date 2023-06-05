import typing as tp

from starlette import status
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.ioc import container, film_services, user_services
from app.exceptions.api import ApiError
from user.dto import (
    FileDTO,
    GetUserFavoriteFilmsDTO,
    ManageFavoriteFilmDTO,
    UpdateProfileDTO,
    UserChangePassword,
    UserChangeEmail,
    ManageWatchStatusFilmDTO,
    GetUserWatchStatusFilmsDTO, UserBase, UserPublicDTO,
)

IFilmService = film_services.IFilmService
IUserService = user_services.IUserService


class MyFavorite(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        user = request.user.instance
        dto = GetUserFavoriteFilmsDTO(**request.query_params, user=user)
        films = await self.__service.get_favorites_films(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())

    @requires("authenticated", status_code=401)
    @requires("active", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.user.instance.id, **data)
        await self.__service.add_film_to_favorite(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    @requires("active", status_code=403)
    async def delete(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.user.instance.id, **data)
        await self.__service.delete_film_from_favorite(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


class UserFavorite(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        user_id = request.path_params["user_id"]
        user = await self.__service.find_user_by_id(user_id)

        dto = GetUserFavoriteFilmsDTO(**request.query_params, user=user)
        films = await self.__service.get_favorites_films(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.path_params["user_id"], **data)
        await self.__service.find_user_by_id(
            dto.user_id
        )  # Если пользователь не существует, будет ошибка
        await self.__service.add_film_to_favorite(dto)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        data = await request.json()
        dto = ManageFavoriteFilmDTO(user_id=request.path_params["user_id"], **data)
        await self.__service.find_user_by_id(
            dto.user_id
        )  # Если пользователь не существует, будет ошибка
        await self.__service.delete_film_from_favorite(dto)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class MyWatchStatus(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        user = request.user.instance
        watch_status = (
            "watching"
            if "q" not in request.query_params.keys()
            else request.query_params["q"]
        )
        dto = GetUserWatchStatusFilmsDTO(
            user=user, watch_status=watch_status, **request.query_params
        )
        films = await self.__service.get_watch_status_films(dto)

        return JSONResponse(status_code=status.HTTP_200_OK, content=films.dict())

    @requires("authenticated", status_code=401)
    @requires("active", status_code=403)
    async def post(self, request: Request):
        data = await request.json()
        dto = ManageWatchStatusFilmDTO(user_id=request.user.instance.id, **data)
        await self.__service.change_watch_status(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=401)
    @requires("active", status_code=403)
    async def delete(self, request: Request):
        data = await request.json()
        dto = ManageWatchStatusFilmDTO(
            user_id=request.user.instance.id, watch_status="not_watching", **data
        )
        await self.__service.change_watch_status(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)


# Profiles
class MyProfile(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        user = request.user.instance
        dto = GetUserFavoriteFilmsDTO(**request.query_params, user=user)
        films = await self.__service.get_favorites_films(dto)

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

    # @requires("authenticated", status_code=401)
    # @requires("admin", status_code=403)
    async def get(self, request: Request):
        user_id = request.path_params["user_id"]
        user = await self.__service.find_user_by_id(user_id)
        is_full_info_available = check_is_full_profile_info_available(user, request)
        if not user.is_public and not is_full_info_available:
            raise ApiError.forbidden("Profile is private")
        dto = GetUserFavoriteFilmsDTO(**request.query_params, user=user)
        films = await self.__service.get_favorites_films(dto)
        if not is_full_info_available:
            user = UserPublicDTO(**user.dict())

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


class MyProfileVisibility(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def put(self, request: Request):
        user = request.user.instance
        new_visibility = await self.__service.toggle_profile_visibility(user)
        return JSONResponse(
            status_code=200,
            content={"is_public": new_visibility}
        )


class ProfileVisibility(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def put(self, request: Request):
        user_id = request.path_params["user_id"]
        user = await self.__service.find_user_by_id(user_id)
        new_visibility = await self.__service.toggle_profile_visibility(user)
        return JSONResponse(
            status_code=200,
            content={"is_public": new_visibility}
        )


class ChangeEmail(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def post(self, request: Request):
        data = await request.json()
        dto = UserChangeEmail(user=request.user.instance, **data)
        await self.__service.request_change_email(dto)
        return Response(status_code=204)


class ChangePassword(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=401)
    async def put(self, request: Request):
        data = await request.json()
        dto = UserChangePassword(user=request.user.instance, **data)
        await self.__service.change_user_password(dto)
        return Response(status_code=204)


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


def check_is_full_profile_info_available(user: UserBase, request: Request) -> bool:
    scopes = request.scope["auth"].scopes
    return "admin" in scopes or ("authenticated" in scopes and request.user.instance.id == user.id)
