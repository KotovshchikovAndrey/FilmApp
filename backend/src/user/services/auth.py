import json
from datetime import datetime
import typing as tp
from abc import ABC, ABCMeta, abstractmethod

from app.exceptions.api import ApiError
from app.utils.OtherUtils import email_validate, generate_code, generate_expired_in
from user.crud.reporitories.user import get_user_repository
from user.dto import (
    UserBase,
    UserRegisterDTO,
    UserVerificationData,
    UserLoginDTO,
    UserRefreshTokenDTO,
    UserLogoutDTO,
)

from user.services.user import IUserService
from user.services.token import ITokenService


class IAuthService(ABC):
    @abstractmethod
    async def register(self, dto: UserRegisterDTO) -> tp.Tuple[str, str]:
        ...

    @abstractmethod
    async def send_verification_code(self, dto: UserVerificationData) -> None:
        ...

    @abstractmethod
    async def request_code(self, email: str, host: str, reason: str) -> None:
        ...

    @abstractmethod
    async def complete_register(self, dto: UserVerificationData) -> UserBase:
        ...

    @abstractmethod
    async def login(self, dto: UserLoginDTO) -> tp.Tuple[str, str]:
        ...

    @abstractmethod
    async def logout(self, dto: UserLogoutDTO) -> None:
        ...

    @abstractmethod
    async def logout_everywhere(self, dto: UserBase) -> None:
        ...

    @abstractmethod
    async def authenticate(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def reset_password(self, dto: ...) -> None:
        ...

    @abstractmethod
    async def refresh_token(self, dto: UserRefreshTokenDTO) -> tp.Tuple[str, str]:
        ...


class JwtAuthService(IAuthService):
    def __init__(self, user_service: IUserService, token_service: ITokenService):
        self.__user_service = user_service
        self.__token_service = token_service

    async def register(self, dto: UserRegisterDTO):
        user = await get_user_repository().find_by_email(email=dto.email)
        if user is not None:
            raise ApiError.conflict("User with this email address already exists")
        if not email_validate(dto.email):
            raise ApiError.bad_request("Invalid email address")
        if len(dto.password) < 8:
            raise ApiError.bad_request(
                message="Password length must be at least 8 characters"
            )
        user = UserBase(**await get_user_repository().create(dto))

        token_payload = {
            "id": user.id,
            "email": user.email,
        }
        access_token = self.__token_service.generate_access_token(payload=token_payload)
        refresh_token = self.__token_service.generate_refresh_token(
            access_token=access_token, payload=token_payload
        )
        await self.__user_service.add_refresh_token(
            user_id=user.id, refresh_token=refresh_token
        )

        return access_token, refresh_token

    async def send_verification_code(self, dto: UserVerificationData):
        await get_user_repository().add_verification_code(dto)
        # TODO: убрать комментарий при деплое!!!
        # self.__user_service.mail_server.send_code(code=dto.code, target_email=dto.email)

    async def request_code(self, email: str, host: str, reason: str):
        await self.__user_service.find_user_by_email(email)
        await self.send_verification_code(
            UserVerificationData(
                ip=host,
                code=generate_code(),
                email=email,
                timestamp=generate_expired_in(),
                reason=reason,
            )
        )

    async def complete_register(self, dto: UserVerificationData):
        user = await get_user_repository().find_by_email_and_code(
            email=dto.email, code=dto.code
        )
        if user is None:
            raise ApiError.forbidden(message="Wrong email or code")
        code_info = json.loads(dict(user).get("value"))

        if user["status"] != "not_verified":
            raise ApiError.forbidden(message="Account already verified")

        if code_info["ip"] != dto.ip:
            raise ApiError.forbidden(message="Code not sent for this device")
        if int(code_info["timestamp"]) < int(datetime.now().timestamp()):
            raise ApiError.forbidden(message="Code has expired, request a new one")
        if code_info["reason"] != "complete-register":
            raise ApiError.forbidden(message="The code is for another process")
        usr = await get_user_repository().verify_user(user["id"])
        return UserBase(**usr)

    async def login(self, dto: UserLoginDTO):
        user = await self.authenticate(dto)

        token_payload = {
            "id": user.id,
            "email": user.email,
        }
        access_token = self.__token_service.generate_access_token(payload=token_payload)
        refresh_token = self.__token_service.generate_refresh_token(
            access_token=access_token, payload=token_payload
        )
        await self.__user_service.add_refresh_token(
            user_id=user.id, refresh_token=refresh_token
        )

        return access_token, refresh_token

    async def logout(self, dto: UserLogoutDTO):
        await get_user_repository().delete_refresh_token(dto.user.id, dto.refresh_token)

    async def logout_everywhere(self, dto: UserBase):
        await get_user_repository().delete_all_refresh_tokens(dto.id)

    async def authenticate(self, dto: UserLoginDTO):
        user = await get_user_repository().authorise_user(dto)
        if user is None:
            raise ApiError.forbidden(message="Wrong email or password")
        if user["status"] == "banned":
            raise ApiError.forbidden(message="Your account has been banned")
        return UserBase(**user)

    async def reset_password(self, dto: ...):
        ...

    async def refresh_token(self, dto: UserRefreshTokenDTO):
        access_token, refresh_token = await self.__token_service.refresh_token(dto)
        return access_token, refresh_token
