import json
import typing as tp
from abc import ABC, abstractmethod
from datetime import datetime

from user.crud.reporitories.user import IUserRepository
from user.dto import UserBase, UserRegisterDTO, UserVerificationData
from app.utils.MailSender import MailSender
from app.core import config
from app.exceptions.api import ApiError
from app.utils.OtherUtils import email_validate, generate_code, generate_expired_in


class IUserService(ABC):
    __repository: IUserRepository

    @abstractmethod
    async def get_current_user(self, id: int) -> UserBase:
        ...

    @abstractmethod
    async def find_user_by_email(self, email: str) -> UserBase:
        ...

    @abstractmethod
    async def create_user(self, dto: UserRegisterDTO) -> UserBase:
        ...

    @abstractmethod
    async def send_verification_code(self, dto: UserVerificationData) -> None:
        ...

    @abstractmethod
    async def request_code(self, email: str, host: str) -> None:
        ...

    @abstractmethod
    async def complete_register(self, dto: UserVerificationData) -> UserBase:
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
        # TODO: убрать комментарий при деплое!!!
        # self.mail_server = MailSender(config.MAIL_LOGIN, config.MAIL_PASSWORD)

    async def get_current_user(self, id: int):
        user = await self.__repository.find_by_id(id=id)
        if user is None:
            raise ApiError.not_found(message="Пользователь не найден")
        return UserBase(**user)

    async def find_user_by_email(self, email: str):
        user = await self.__repository.find_by_email(email=email)
        if user is None:
            raise ApiError.not_found(message="Пользователь не найден")
        return UserBase(**user)

    async def create_user(self, dto: UserRegisterDTO):
        user = await self.__repository.find_by_email(email=dto.email)
        if user is not None:
            raise ApiError.conflict(
                "Пользователь с таким адресом электронной почты уже существует"
            )
        if not email_validate(dto.email):
            raise ApiError.bad_request("Введён некорректный адрес электронной почты")
        user = await self.__repository.create(dto)
        return UserBase(**user)

    async def send_verification_code(self, dto: UserVerificationData):
        await self.__repository.add_verification_code(dto)
        # TODO: убрать комментарий при деплое!!!
        # self.mail_server.send_code(code=dto.code, target_email=dto.email)

    async def request_code(self, email: str, host: str):
        user = await self.find_user_by_email(email)
        await self.send_verification_code(
            UserVerificationData(
                ip=host,
                id=user.id,
                code=generate_code(),
                email=email,
                timestamp=generate_expired_in(),
            )
        )

    async def complete_register(self, dto: UserVerificationData):
        user = await self.__repository.find_by_email_and_code(
            email=dto.email, code=dto.code
        )
        if user is None:
            raise ApiError.forbidden(message="Неверная связка пользователь-код")
        code_info = json.loads(dict(user).get("value"))

        if code_info["ip"] != dto.ip:
            raise ApiError.forbidden(
                message="Код был отправлен не для этого устройства"
            )
        if (
            datetime.strptime(code_info["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
            < datetime.now()
        ):
            raise ApiError.forbidden(message="Код просрочен. Запросите новый.")
        await self.__repository.verify_user(user["id"])
        usr = UserBase(**user).status = "active"
        return usr

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
