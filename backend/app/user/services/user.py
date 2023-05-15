import typing as tp
from abc import ABC, abstractmethod

from user.crud.reporitories.user import IUserRepository
from user.dto import UserBase


class IUserService(ABC):
    __repository: IUserRepository

    @abstractmethod
    async def get_current_user(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def find_user_by_email(self, email: str) -> UserBase:
        ...

    @abstractmethod
    async def create_user(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def update_user(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def delete_user(self, dto: ...) -> None:
        ...

    @abstractmethod
    async def update_reset_token(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def add_to_favorite(self, dto: ...) -> None:
        ...


class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.__repository = repository

    async def get_current_user(self, dto: ...):
        ...

    async def find_user_by_email(self, email: str):
        user = await self.__repository.find_by_email(email=email)
        return UserBase(**user)

    async def create_user(self, dto: ...):
        ...

    async def update_user(self, dto: ...):
        ...

    async def delete_user(self, dto: ...):
        ...

    async def update_reset_token(self, dto: ...):
        ...

    async def add_to_favorite(self, dto: ...) -> None:
        ...

    async def __generate_reset_token(self, token: str) -> str:
        ...
