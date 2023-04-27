import typing as tp
from abc import ABC, ABCMeta, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    async def regiter(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def login(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def logout(self, dto: ...) -> None:
        ...

    @abstractmethod
    async def authenticate(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def reset_password(self, dto: ...) -> None:
        ...


class JwtAuthService(IAuthService):
    __user_service: ...
    __token_service: ...

    def __init__(self, user_service: ..., token_service: ...):
        ...

    async def register(self, dto: ...):
        ...

    async def login(self, dto: ...):
        ...

    async def logout(self, dto: ...):
        ...

    async def authenticate(self, dto: ...):
        ...

    async def reset_password(self, dto: ...):
        ...
