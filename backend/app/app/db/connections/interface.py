import typing as tp
from abc import ABC, abstractmethod


class IDbConnection(ABC):
    @abstractmethod
    async def connect(self) -> None:
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        ...

    @abstractmethod
    async def execute_query(self, query: str) -> ...:
        ...

    @abstractmethod
    def get_url(self) -> str:
        ...
