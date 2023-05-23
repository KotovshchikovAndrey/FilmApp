import json
import typing as tp
from abc import ABC, abstractmethod
from datetime import datetime

from app.utils.MailSender import MailSender
from app.core import config

from user.crud.reporitories.user import IUserRepository
from film.services import IFilmService

# from app.core.ioc import
from film.dto import FilmsDTO
from user.dto import UserBase, UserRegisterDTO, AddFavoriteFilmDTO
from app.exceptions.api import ApiError
from app.utils.OtherUtils import email_validate, generate_code, generate_expired_in


class IUserService(ABC):
    __repository: IUserRepository
    __film_service: IFilmService

    # TODO: убрать комментарий при деплое!!!
    # mail_server: MailSender

    @abstractmethod
    async def get_current_user(self, id: int) -> UserBase:
        ...

    @abstractmethod
    async def find_user_by_email(self, email: str) -> UserBase:
        ...

    @abstractmethod
    async def find_user_by_id(self, target_id: int) -> UserBase:
        ...

    @abstractmethod
    async def check_user_exists(self, email: str) -> bool:
        ...

    @abstractmethod
    async def create_user(self, dto: UserRegisterDTO) -> UserBase:
        ...

    @abstractmethod
    async def update_user(self, dto: ...) -> ...:
        ...

    @abstractmethod
    async def delete_user(self, dto: ...) -> None:
        ...

    @abstractmethod
    async def add_refresh_token(self, user_id: int, refresh_token: str) -> None:
        ...

    @abstractmethod
    async def add_to_favorite(self, dto: AddFavoriteFilmDTO) -> None:
        ...

    @abstractmethod
    async def get_favorites(self, user_id: int) -> FilmsDTO:
        ...


class UserService(IUserService):
    def __init__(self, repository: IUserRepository, film_service: IFilmService):
        self.__repository = repository
        self.__film_service = film_service
        # TODO: убрать комментарий при деплое!!!
        # self.mail_server = MailSender(config.MAIL_LOGIN, config.MAIL_PASSWORD)

    async def get_current_user(self, id: int):
        user = await self.__repository.find_by_id(target_id=id)
        if user is None:
            raise ApiError.not_found(message="User not found")
        return UserBase(**user)

    async def find_user_by_email(self, email: str):
        user = await self.__repository.find_by_email(email=email)
        if user is None:
            raise ApiError.not_found(message="User not found")
        return UserBase(**user)

    async def find_user_by_id(self, target_id: int):
        user = await self.__repository.find_by_id(target_id=target_id)
        if user is None:
            raise ApiError.not_found(message="User not found")
        return UserBase(**user)

    async def check_user_exists(self, email: str):
        user = await self.__repository.find_by_email(email=email)
        return user is not None

    async def create_user(self, dto: UserRegisterDTO):
        is_user_exist = await self.check_user_exists(email=dto.email)
        if is_user_exist:
            raise ApiError.conflict("User with this email already exists")
        if not email_validate(dto.email):
            raise ApiError.bad_request("Invalid email address")
        user = await self.__repository.create(dto)
        return UserBase(**user)

    async def update_user(self, dto: ...):
        ...

    async def delete_user(self, dto: ...):
        ...

    async def add_refresh_token(self, user_id: int, refresh_token: str):
        await self.__repository.add_refresh_token(user_id, refresh_token)

    async def add_to_favorite(self, dto: AddFavoriteFilmDTO):
        film = await self.__film_service.get_film_info(dto.film_id)
        await self.__repository.add_to_favorite(user_id=dto.user.id, film_id=film.id)

    async def get_favorites(self, user_id: int):
        return await self.__film_service.get_user_favorite_films(user_id)

    async def __generate_reset_token(self, token: str) -> str:
        ...
