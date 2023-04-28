from __future__ import annotations

import typing as tp
import databases
from app.db.connections.interface import IDbConnection


class PostgresConnection(IDbConnection):
    __instance: tp.Optional[PostgresConnection] = None
    __connection: databases.Database

    __db_user: str
    __db_password: str
    __db_host: str
    __db_port: str
    __db_name: str

    def __new__(cls, *args: tp.Any, **kwargs: tp.Any):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(
        self,
        db_user: str,
        db_password: str,
        db_host: str,
        db_port: str,
        db_name: str,
    ):
        self.__db_user = db_user
        self.__db_password = db_password
        self.__db_host = db_host
        self.__db_port = db_port
        self.__db_name = db_name

        self.__connection = databases.Database(url=self.get_url())

    async def connect(self):
        await self.__connection.connect()

    async def disconnect(self):
        if self.__connection.is_connected:
            await self.__connection.disconnect()

    async def execute_query(self, query: str):
        result = await self.__connection.execute(query)
        return result

    def get_url(self):
        db_url = f"postgresql+psycopg2://{self.__db_user}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"
        return db_url
