import typing as tp
from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def find_by_id(self, email: str) -> ...:
        ...

    @abstractmethod
    async def update(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def add_to_favorite(self, user_id: int, car_id: int):
        ...


class UserPostgresRepository(IUserRepository):
    async def create(self, **kwargs: ...):
        ...

    async def find_by_id(self, email: str):
        ...

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int):
        ...

    async def add_to_favorite(self, user_id: int, car_id: int):
        ...
