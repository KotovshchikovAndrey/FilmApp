from __future__ import annotations

import typing as tp
from starlette.applications import Starlette


class StarletteServer:
    __instance: tp.Optional[StarletteServer] = None

    __app: Starlette
    __db_connection: ...

    def __new__(cls, *args: tp.Any, **kwargs: tp.Any):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self, is_debug: bool = False) -> None:
        pass

    async def __handle_error(self, exc: Exception):
        ...

    async def __handle_startup(self):
        ...

    async def __handle_shutdown(self):
        ...

    async def __connect_db(self):
        ...

    @property
    def app(self):
        return self.__app
