from __future__ import annotations

import typing as tp

import pydantic
from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount

from app.core import config
from app.db import IDbConnection, db_connection
from app.exceptions.api import ApiError


class StarletteServer:
    __instance: tp.Optional[StarletteServer] = None

    __app: Starlette
    __db_connection: IDbConnection

    def __new__(cls, *args: tp.Any, **kwargs: tp.Any):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(
        self,
        routes: tp.Iterable[Mount],
        middlewares: tp.Iterable[Middleware],
        is_debug: bool = False,
    ) -> None:
        self.__app = Starlette(
            routes=routes,
            middleware=middlewares,
            on_startup=[self.__handle_startup],
            on_shutdown=[self.__handle_shutdown],
            exception_handlers={Exception: self.__handle_error},
            debug=is_debug,
        )

        self.__db_connection = db_connection

    def get_app_instance(self):
        return self.__app

    async def __handle_error(self, request: Request, exc: Exception):
        if isinstance(exc, ApiError):
            response = JSONResponse(
                status_code=exc.status,
                content={"message": exc.message, "details": exc.details},
            )
        elif isinstance(exc, pydantic.ValidationError):
            response = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Invalid data", "details": exc.errors()},
            )
        else:
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Internal Server Error", "details": []},
            )

        await self.__set_cors_headers(request, response)
        return response

    async def __handle_startup(self):
        await self.__db_connection.connect()

    async def __handle_shutdown(self):
        await self.__db_connection.disconnect()

    async def __set_cors_headers(self, request: Request, response: Response):
        if "*" in config.ALLOW_ORIGINS:
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return

        client_origin = request.headers.get("origin", None)
        if client_origin is None:
            return

        if client_origin not in config.ALLOW_ORIGINS:
            return

        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Origin"] = client_origin
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
