import typing as tp
from abc import ABC, abstractmethod


class IUserService(ABC):
    __repository: ...

    @abstractmethod
    async def get_current_user(self, dto: ...) -> ...:
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
    def __init__(self, repository: ...):
        ...

    async def get_current_user(self, dto: ...):
        ...

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
