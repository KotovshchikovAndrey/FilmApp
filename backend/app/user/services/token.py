import datetime
import typing as tp
from abc import ABC, abstractmethod

import jwt
from app.core import config
from user.crud.reporitories import IUserRepository
from user.crud.reporitories.user import get_user_repository


class ITokenService(ABC):
    __repository: IUserRepository

    @abstractmethod
    async def refresh_token(self, dto: ...) -> ...:
        ...

    @abstractmethod
    def generate_access_token(self, payload: tp.Dict[str, tp.Any]) -> str:
        ...

    @abstractmethod
    def generate_refresh_token(self, access_token: str, payload: tp.Dict[str, tp.Any]) -> str:
        ...

    @abstractmethod
    async def decode_token(self, dto: ...) -> ...:
        ...


class TokenService(ITokenService):
    def __init__(self, repository: IUserRepository = get_user_repository()):
        self.__repository = repository

    async def refresh_token(self, dto: ...):
        ...

    def generate_access_token(self, payload: tp.Dict[str, tp.Any]) -> str:
        additional_payload = {"exp": int(datetime.datetime.now().timestamp()) + 60 * 30}
        payload.update(additional_payload)
        token = jwt.encode(payload, str(config.SECRET_KEY), "HS256")
        return token

    def generate_refresh_token(self, access_token: str, payload: tp.Dict[str, tp.Any]) -> str:
        additional_payload = {"exp": int(datetime.datetime.now().timestamp()) + 3600 * 24 * 90}
        payload.update(additional_payload)
        token = jwt.encode(payload, str(config.SECRET_KEY) + self.__get_access_token_part(access_token), "HS256")
        return token

    async def decode_token(self, dto: ...):
        ...

    def __get_access_token_part(self, token: str) -> str:
        signature = token.split('.')[-1]
        signature_len = len(signature)
        return signature[signature_len // 4:signature_len // 2]


token_service = TokenService()


def get_token_service() -> ITokenService:
    return token_service
