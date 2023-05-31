import datetime
import typing as tp
from abc import ABC, abstractmethod

import jwt

from app.core import config
from app.exceptions.api import ApiError
from user.crud.reporitories import IUserRepository
from user.dto import UserRefreshTokenDTO


class ITokenService(ABC):
    __repository: IUserRepository

    @abstractmethod
    async def refresh_token(self, dto: UserRefreshTokenDTO) -> tp.Tuple[str, str]:
        ...

    @abstractmethod
    def generate_access_token(self, payload: tp.Dict[str, tp.Any]) -> str:
        ...

    @abstractmethod
    def generate_refresh_token(
            self, access_token: str, payload: tp.Dict[str, tp.Any]
    ) -> str:
        ...

    @abstractmethod
    def decode_access_token(self, access_token: str) -> tp.Dict[str, tp.Any]:
        ...

    @abstractmethod
    def decode_refresh_token(
            self, access_token: str, refresh_token: str
    ) -> tp.Dict[str, tp.Any]:
        ...

    @abstractmethod
    def generate_a_pair_of_tokens(self, user_id: int) -> tp.Tuple[str, str]:
        ...


class TokenService(ITokenService):
    def __init__(self, repository: IUserRepository):
        self.__repository = repository

    async def refresh_token(self, dto: UserRefreshTokenDTO):
        payload = self.decode_refresh_token(dto.access_token, dto.refresh_token)
        is_refresh_valid = await self.__repository.check_refresh_token(
            payload["id"], dto.refresh_token
        )
        if not is_refresh_valid:
            raise ApiError.forbidden(message="Refresh token has been revoked")
        access_token = self.generate_access_token(payload)
        refresh_token = self.generate_refresh_token(access_token, payload)
        await self.__repository.replace_refresh_token(
            payload["id"], dto.refresh_token, refresh_token
        )
        return access_token, refresh_token

    def generate_access_token(self, payload: tp.Dict[str, tp.Any]) -> str:
        additional_payload = {"exp": int(datetime.datetime.now().timestamp()) + 60 * 15}
        payload.update(additional_payload)
        token = jwt.encode(payload, str(config.SECRET_KEY), "HS256")
        return token

    def generate_refresh_token(
            self, access_token: str, payload: tp.Dict[str, tp.Any]
    ) -> str:
        additional_payload = {
            "exp": int(datetime.datetime.now().timestamp()) + 3600 * 24 * 90
        }
        payload.update(additional_payload)
        token = jwt.encode(
            payload,
            str(config.SECRET_KEY) + self.__get_access_token_part(access_token),
            "HS256",
        )
        return token

    def decode_access_token(self, access_token: str) -> tp.Dict[str, tp.Any]:
        payload = jwt.decode(access_token, str(config.SECRET_KEY), ["HS256"])
        return payload

    def decode_refresh_token(self, access_token: str, refresh_token: str):
        access_token_part = self.__get_access_token_part(access_token)
        try:
            payload = jwt.decode(
                refresh_token, str(config.SECRET_KEY) + access_token_part, ["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise ApiError.unauthorized(message="Refresh token has expired")
        except jwt.InvalidTokenError:
            raise ApiError.forbidden(message="Wrong token")
        return payload

    def __get_access_token_part(self, token: str) -> str:
        signature = token.split(".")[-1]
        signature_len = len(signature)
        return signature[signature_len // 4 : signature_len // 2]

    def generate_a_pair_of_tokens(self, user_id: int) -> tp.Tuple[str, str]:
        token_payload = {
            "id": user_id,
        }
        access_token = self.generate_access_token(payload=token_payload)
        refresh_token = self.generate_refresh_token(
            access_token=access_token, payload=token_payload
        )
        return access_token, refresh_token
