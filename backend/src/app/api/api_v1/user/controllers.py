import typing as tp

from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint

from user.dto import AddFavoriteFilmDTO
from app.core.ioc import container, user_services

IUserService = user_services.IUserService


class UserFavorite(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def get(self, request: Request):
        ...

    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def post(self, request: Request):
        data = await request.json()
        dto = AddFavoriteFilmDTO(user=request.user.instance, **data)
        await self.__service.add_to_favorite(dto)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def delete(self, request: Request):
        ...


class Profile(HTTPEndpoint):
    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def get(self, request: Request):
        ...

    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def delete(self, request: Request):
        ...
