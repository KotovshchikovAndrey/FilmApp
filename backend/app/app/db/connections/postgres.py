import typing as tp
from app.db.connections.interface import IDbConnection


class PostgresConnection(IDbConnection):
    def __init__(self):
        ...

    async def connect(self):
        ...

    async def disconnect(self):
        ...

    async def execute_query(self, query: str):
        ...

    async def get_url(self):
        ...
