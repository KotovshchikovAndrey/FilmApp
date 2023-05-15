import typing as tp
from abc import ABC, abstractmethod

from app.db import db_connection
from user.crud import queries


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def find_by_email(self, email: str) -> tp.Mapping:
        ...

    @abstractmethod
    async def find_by_id(self, id: int) -> ...:
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

    async def find_by_email(self, email: str):
        user = await db_connection.fetch_one(
            queries.FIND_USER_BY_EMAIL,
            email=email
        )
        return user

    async def find_by_id(self, id: int):
        ...

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int):
        ...

    async def add_to_favorite(self, user_id: int, car_id: int):
        ...
