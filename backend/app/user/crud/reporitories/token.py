import typing as tp
from abc import ABC, abstractmethod


class ITokenReporitory(ABC):
    @abstractmethod
    async def create(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def find_by_value(self, user_id: int, value: str) -> ...:
        ...

    @abstractmethod
    async def update(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def delete(self, user_id: int, value: str) -> None:
        ...


class TokenPostgresRepository(ITokenReporitory):
    async def create(self, **kwargs: ...):
        ...

    async def find_by_value(self, user_id: int, value: str):
        ...

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int, value: str):
        ...
