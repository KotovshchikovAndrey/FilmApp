import typing as tp
from abc import ABC, abstractmethod


class ITokenService(ABC):
    __repository: ...

    @abstractmethod
    async def refresh_token(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def generate_access_token(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def generate_refresh_token(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def decode_token(self, dto: ...) -> ...:
        ...


class TokenService(ITokenService):
    def __init__(self, repository: ...):
        ...

    async def refresh_token(self, dto: ...):
        ...

    async def generate_access_token(self, dto: ...):
        ...

    async def generate_refresh_token(self, dto: ...):
        ...

    async def decode_token(self, dto: ...):
        ...

    async def __get_access_token_part(self, token: str) -> str:
        ...
