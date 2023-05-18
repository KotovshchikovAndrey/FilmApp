from __future__ import annotations

import typing as tp

import pydantic

from starlette import status
from starlette.requests import Request
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from app.exceptions.api import ApiError
from app.db import IDbConnection, db_connection


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
            return JSONResponse(
                status_code=exc.status,
                content={"message": exc.message, "details": exc.details},
            )

        if isinstance(exc, pydantic.ValidationError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Invalid data", "details": exc.errors()},
            )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error", "details": []},
        )

    async def __handle_startup(self):
        await self.__db_connection.connect()

    async def __handle_shutdown(self):
        await self.__db_connection.disconnect()
