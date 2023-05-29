import json
import typing as tp
from abc import ABC, abstractmethod
from datetime import datetime

from app.exceptions.api import ApiError
from app.utils.OtherUtils import email_validate, generate_code, generate_expired_in
from user.crud.reporitories.user import get_user_repository
from user.dto import (
    UserBase,
    UserLoginDTO,
    UserLogoutDTO,
    UserRefreshTokenDTO,
    UserRegisterDTO,
    UserRequestCodeDTO,
)
from user.services.token import ITokenService
from user.services.user import IUserService


class IAuthService(ABC):
    @abstractmethod
    async def register(self, dto: UserRegisterDTO) -> tp.Tuple[str, str]:
        ...

    @abstractmethod
    async def send_verification_code(self, dto: UserRequestCodeDTO) -> None:
        ...

    @abstractmethod
    async def request_code(self, email: str, reason: str) -> None:
        ...

    @abstractmethod
    async def redeem_code(self, dto: UserRequestCodeDTO) -> None:
        ...

    @abstractmethod
    async def login(self, dto: UserLoginDTO) -> tp.Tuple[str, str, str]:
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

    @abstractmethod
    async def decode_access_token(self, access_token: str) -> tp.Dict[str, tp.Any]:
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
        if not 8 <= len(dto.password) <= 100:
            raise ApiError.bad_request(
                message="Password length must be between 8 and 100 characters"
            )
        user = UserBase(**await get_user_repository().create(dto))

        access_token, refresh_token = self.__token_service.generate_a_pair_of_tokens(user.id)
        await self.__user_service.add_refresh_token(
            user_id=user.id, refresh_token=refresh_token
        )

        return access_token, refresh_token

    async def send_verification_code(self, dto: UserRequestCodeDTO):
        await get_user_repository().add_verification_code(dto.dict())
        #TODO: убрать комментарий при деплое!!!
        # self.__user_service.mail_server.send_code(code=dto.code, target_email=dto.email)

    async def request_code(self, email: str, reason: str):
        user = await self.__user_service.find_user_by_email(email)
        if user.status != "not-verified":
            raise ApiError.forbidden(message="Account already verified")
        await self.send_verification_code(
            UserRequestCodeDTO(
                code=generate_code(),
                email=email,
                timestamp=generate_expired_in(),
                reason=reason,
            )
        )

    async def redeem_code(self, dto: UserRequestCodeDTO):
        user = await get_user_repository().find_by_email_and_code(
            email=dto.email, code=dto.code
        )
        if user is None:
            raise ApiError.forbidden(message="Wrong code")
        code_info = json.loads(dict(user).get("value"))
        if code_info["timestamp"] < int(datetime.now().timestamp()):
            raise ApiError.forbidden(message="Code has expired, request a new one")

        match code_info["reason"]:
            case "change-email":
                is_email_assigned = await self.__user_service.check_user_exists(code_info["email"])
                if is_email_assigned:
                    raise ApiError.conflict(message="This email address is already in use")
                await get_user_repository().change_email(user["id"], code_info["email"])
                if user["status"] == "not_verified":
                    await get_user_repository().verify_user(user["id"])
            case "complete-register":
                if user["status"] != "not_verified":
                    raise ApiError.forbidden(message="Account already verified")
                await get_user_repository().verify_user(user["id"])
            case _:
                raise ApiError.internal("The code in the database has an unknown reason")

    async def login(self, dto: UserLoginDTO):
        user = await self.authenticate(dto)

        access_token, refresh_token = self.__token_service.generate_a_pair_of_tokens(user.id)
        await self.__user_service.add_refresh_token(
            user_id=user.id, refresh_token=refresh_token
        )

        return access_token, refresh_token, user.status

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

    async def decode_access_token(self, access_token: str):
        payload = await self.__token_service.decode_access_token(access_token)
        return payload
