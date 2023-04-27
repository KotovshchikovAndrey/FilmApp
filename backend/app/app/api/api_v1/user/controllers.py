import typing as tp

from starlette import status
from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint


class UserFavorite(HTTPEndpoint):
    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def get(self, request: Request):
        ...

    @requires("authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    async def post(self, request: Request):
        ...

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
