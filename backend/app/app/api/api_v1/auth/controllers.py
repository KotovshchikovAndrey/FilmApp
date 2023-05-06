import typing as tp

from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint


class Registration(HTTPEndpoint):
    async def post(self, request: Request):
        ...


class Login(HTTPEndpoint):
    async def post(self, request: Request):
        ...


class TokenRefresh(HTTPEndpoint):
    async def update(self, request: Request):
        ...


class Logout(HTTPEndpoint):
    async def delete(self, request: Request):
        ...
