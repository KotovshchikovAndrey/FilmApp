import typing as tp

from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint


class MyFavorite(HTTPEndpoint):
    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    async def post(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        ...


class UserFavorite(HTTPEndpoint):
    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        ...

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
    @requires("authenticated", status_code=401)
    async def get(self, request: Request):
        user = request.user.instance

    @requires("authenticated", status_code=401)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    async def delete(self, request: Request):
        ...


class Profile(HTTPEndpoint):
    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def get(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def update(self, request: Request):
        ...

    @requires("authenticated", status_code=401)
    @requires("admin", status_code=403)
    async def delete(self, request: Request):
        ...
