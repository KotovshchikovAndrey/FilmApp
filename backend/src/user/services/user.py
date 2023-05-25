import json
import typing as tp
from abc import ABC, abstractmethod
from datetime import datetime

from app.core import config
from app.exceptions.api import ApiError
from app.utils.file_manager import FileManager
from app.utils.MailSender import MailSender
from app.utils.OtherUtils import email_validate, generate_code, generate_expired_in
from film.dto import FilmsDTO
from film.services import IFilmService
from user.crud.reporitories import IUserRepository
from user.dto import (
    FileDTO,
    GetUserFavoriteFilmsDTO,
    ManageFavoriteFilmDTO,
    UpdateProfileDTO,
    UserAvatarDTO,
    UserBase,
    UserRegisterDTO,
)


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
    async def update_user_profile(self, user: UserBase, dto: UpdateProfileDTO) -> None:
        ...

    @abstractmethod
    async def set_user_avatar(self, user: UserBase, dto: FileDTO) -> UserAvatarDTO:
        ...

    @abstractmethod
    async def delete_user(self, dto: ...) -> None:
        ...

    @abstractmethod
    async def ban_user(self, target_id: int) -> None:
        ...

    @abstractmethod
    async def unban_user(self, target_id: int) -> None:
        ...

    @abstractmethod
    async def add_refresh_token(self, user_id: int, refresh_token: str) -> None:
        ...

    @abstractmethod
    async def add_to_favorite(self, dto: ManageFavoriteFilmDTO) -> None:
        ...

    @abstractmethod
    async def delete_from_favorite(self, dto: ManageFavoriteFilmDTO) -> None:
        ...

    @abstractmethod
    async def get_favorites(self, dto: GetUserFavoriteFilmsDTO) -> FilmsDTO:
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

    async def update_user_profile(self, user: UserBase, dto: UpdateProfileDTO) -> None:
        return await self.__repository.update_profile_fields(
            user_id=user.id, profile_update=dto
        )

    async def set_user_avatar(self, user: UserBase, dto: FileDTO):
        file_manager = FileManager(upload_dir=config.UPLOAD_DIR + "/avatars")
        avatar = await file_manager.upload(filename=dto.filename, file=dto.content)

        return await self.__repository.set_avatar(user_id=user.id, avatar=avatar)

    async def delete_user(self, dto: ...):
        ...

    async def add_refresh_token(self, user_id: int, refresh_token: str):
        await self.__repository.add_refresh_token(user_id, refresh_token)

    async def add_to_favorite(self, dto: ManageFavoriteFilmDTO):
        film = await self.__film_service.get_film_info(dto.film_id)
        await self.__repository.add_to_favorite(user_id=dto.user_id, film_id=film.id)

    async def delete_from_favorite(self, dto: ManageFavoriteFilmDTO):
        film = await self.__film_service.get_film_info(dto.film_id)
        await self.__repository.delete_from_favorite(
            user_id=dto.user_id, film_id=film.id
        )

    async def get_favorites(self, dto: GetUserFavoriteFilmsDTO):
        user, order_by = dto.user, dto.order_by.value
        films = await self.__film_service.get_user_favorite_films(
            target_id=user.id, order_by=order_by
        )

        return films

    async def ban_user(self, target_id: int):
        user = await self.find_user_by_id(target_id)
        if user.role == "admin":
            raise ApiError.conflict(message="You can't ban admin")
        await self.__repository.ban_user(target_id)

    async def unban_user(self, target_id: int):
        user = await self.find_user_by_id(target_id)
        if user.role == "admin":
            raise ApiError.conflict(message="You can't unban admin")
        await self.__repository.unban_user(target_id)

    async def __generate_reset_token(self, token: str) -> str:
        ...
