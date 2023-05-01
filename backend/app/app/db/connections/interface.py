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
    async def fetch_one(self, query: str, **params: tp.Any) -> tp.Any:
        ...

    @abstractmethod
    async def fetch_all(self, query: str, **params: tp.Any) -> tp.Iterable[tp.Any]:
        ...

    @abstractmethod
    async def execute_query(self, query: str, **params: tp.Any) -> None:
        ...

    @abstractmethod
    def get_url(self) -> str:
        ...
