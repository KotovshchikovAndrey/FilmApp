import typing as tp

from starlette import status
from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint


class Film(HTTPEndpoint):
    async def get(self, request: Request):
        ...

    async def post(self, request: Request):
        ...


class FilmDetail(HTTPEndpoint):
    async def get(self, request: Request):
        ...

    @requires("admin", status_code=status.HTTP_403_FORBIDDEN)
    async def update(self, request: Request):
        ...

    @requires("admin", status_code=status.HTTP_403_FORBIDDEN)
    async def delete(self, request: Request):
        ...


class FilmSearch(HTTPEndpoint):
    async def get(self, request: Request):
        ...
