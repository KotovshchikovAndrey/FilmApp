import json
import typing as tp
from abc import ABC, abstractmethod

from app.db import db_connection
from app.utils.OtherUtils import get_password_hash
from user.crud import queries
from user.dto import (
    UpdateProfileDTO,
    UserAvatarDTO,
    UserLoginDTO,
    UserRegisterDTO,
)


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, dto: UserRegisterDTO) -> tp.Mapping:
        ...

    @abstractmethod
    async def find_by_email(self, email: str) -> tp.Mapping:
        ...

    @abstractmethod
    async def find_by_email_and_code(self, email: str, code: str) -> tp.Mapping:
        ...

    @abstractmethod
    async def verify_user(self, id: int) -> None:
        ...

    @abstractmethod
    async def clear_codes(self, id: int) -> None:
        ...

    @abstractmethod
    async def authorise_user(self, dto: UserLoginDTO) -> tp.Mapping:
        ...

    @abstractmethod
    async def add_verification_code(self, code_info: dict) -> tp.Mapping:
        ...

    @abstractmethod
    async def find_by_id(self, target_id: int) -> tp.Mapping:
        ...

    @abstractmethod
    async def update_profile_fields(
            self, user_id: int, profile_update: UpdateProfileDTO
    ) -> None:
        ...

    @abstractmethod
    async def change_email(self, user_id: int, new_email: str) -> None:
        ...

    @abstractmethod
    async def set_avatar(self, user_id: int, avatar: str) -> UserAvatarDTO:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def ban_user(self, target_id: int) -> None:
        ...

    @abstractmethod
    async def unban_user(self, target_id: int) -> None:
        ...

    @abstractmethod
    async def change_watch_status(self, user_id: int, film_id: int, watch_status: str):
        ...

    @abstractmethod
    async def add_to_favorite(self, user_id: int, film_id: int):
        ...

    @abstractmethod
    async def delete_from_favorite(self, user_id: int, film_id: int):
        ...

    @abstractmethod
    async def add_refresh_token(self, user_id: int, refresh_token: str):
        ...

    @abstractmethod
    async def delete_refresh_token(self, user_id: int, refresh_token: str):
        ...

    @abstractmethod
    async def delete_all_refresh_tokens(self, user_id: int):
        ...

    @abstractmethod
    async def replace_refresh_token(
            self, target_id: int, old_token: str, new_token: str
    ):
        ...

    @abstractmethod
    async def check_refresh_token(self, target_id: int, refresh_token: str) -> bool:
        ...

    @abstractmethod
    async def check_password(self, target_id: int, password: str) -> bool:
        ...

    @abstractmethod
    async def change_password(self, target_id: int, password: str) -> None:
        ...


class UserPostgresRepository(IUserRepository):
    async def create(self, dto: UserRegisterDTO):
        await db_connection.execute_query(
            queries.CREATE_NEW_USER,
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            password=get_password_hash(dto.password),
        )
        user = await db_connection.fetch_one(
            queries.FIND_USER_BY_EMAIL, email=dto.email
        )
        return user

    async def find_by_email(self, email: str):
        user = await db_connection.fetch_one(queries.FIND_USER_BY_EMAIL, email=email)
        return user

    async def find_by_email_and_code(self, email: str, code: str):
        user = await db_connection.fetch_one(
            queries.FIND_USER_WITH_CODE, email=email, code=code
        )
        return user

    async def find_by_id(self, target_id: int):
        user = await db_connection.fetch_one(queries.FIND_USER_BY_ID, id=target_id)
        return user

    async def verify_user(self, id: int):
        await db_connection.execute_query(
            queries.VERIFY_USER,
            id=id,
        )

    async def clear_codes(self, id: int):
        await db_connection.execute_query(
            queries.CLEAR_CODES,
            id=id,
        )

    async def authorise_user(self, dto: UserLoginDTO):
        user = await db_connection.fetch_one(
            queries.AUTHORISE_USER,
            email=dto.email,
            password=get_password_hash(dto.password),
        )
        return user

    async def add_verification_code(self, code_info: dict):
        await db_connection.execute_query(
            queries.ADD_NEW_VERIFICATION_CODE.replace(
                "PASTE_JSON_HERE",
                f"'{json.dumps(code_info)}'",
            ),
            email=code_info["email"],
        )

    async def update_profile_fields(
            self, user_id: int, profile_update: UpdateProfileDTO
    ):
        return await db_connection.execute_query(
            queries.UPDATE_PROFILE_FIELDS,
            user_id=user_id,
            **profile_update.dict(),
        )

    async def change_email(self, user_id: int, new_email: str):
        await db_connection.execute_query(
            queries.CHANGE_USER_EMAIL,
            user_id=user_id,
            new_email=new_email,
        )

    async def set_avatar(self, user_id: int, avatar: str):
        avatar_url = await db_connection.fetch_one(
            queries.SET_AVATAR_FOR_USER, user_id=user_id, avatar=avatar
        )

        return UserAvatarDTO(**avatar_url)

    async def delete(self, user_id: int):
        ...

    async def ban_user(self, target_id: int):
        await db_connection.execute_query(
            queries.CHANGE_USER_STATUS,
            status="banned",
            id=target_id,
        )
        await db_connection.execute_query(
            queries.DELETE_ALL_REFRESH_TOKENS,
            id=target_id,
        )

    async def unban_user(self, target_id: int):
        await db_connection.execute_query(
            queries.CHANGE_USER_STATUS,
            status="active",
            id=target_id,
        )

    async def change_watch_status(self, user_id: int, film_id: int, watch_status: str):
        await db_connection.execute_query(
            queries.CHANGE_WATCH_STATUS,
            user_id=user_id,
            film_id=film_id,
            watch_status=watch_status,
        )

    async def add_to_favorite(self, user_id: int, film_id: int):
        await db_connection.execute_query(
            queries.ADD_FAVORITE_FILM_FOR_USER,
            user_id=user_id,
            film_id=film_id,
        )

    async def delete_from_favorite(self, user_id: int, film_id: int):
        await db_connection.execute_query(
            queries.DELETE_FAVORITE_FILM_FROM_USER,
            user_id=user_id,
            film_id=film_id,
        )

    async def add_refresh_token(self, user_id: int, refresh_token: str):
        await db_connection.execute_query(
            queries.ADD_REFRESH_TOKEN,
            refresh_token=refresh_token,
            id=user_id,
        )

    async def delete_refresh_token(self, user_id: int, refresh_token: str):
        await db_connection.execute_query(
            queries.DELETE_REFRESH_TOKEN,
            refresh_token=refresh_token,
            id=user_id,
        )

    async def delete_all_refresh_tokens(self, user_id: int):
        await db_connection.execute_query(
            queries.DELETE_ALL_REFRESH_TOKENS,
            id=user_id,
        )

    async def replace_refresh_token(
            self, target_id: int, old_token: str, new_token: str
    ):
        await db_connection.execute_query(
            queries.UPDATE_REFRESH_TOKEN,
            old_token=old_token,
            new_token=new_token,
            target_id=target_id,
        )

    async def check_refresh_token(self, target_id: int, refresh_token: str) -> bool:
        user = await db_connection.fetch_one(
            queries.CHECK_REFRESH_TOKEN,
            target_id=target_id,
            refresh_token=refresh_token,
        )
        return user is not None

    async def check_password(self, target_id: int, password: str) -> bool:
        user = await db_connection.fetch_one(
            queries.CHECK_PASSWORD,
            id=target_id,
            password=get_password_hash(password),
        )
        return user is not None

    async def change_password(self, target_id: int, password: str):
        await db_connection.execute_query(
            queries.CHANGE_USER_PASSWORD,
            id=target_id,
            password=get_password_hash(password),
        )


user_repository = UserPostgresRepository()


def get_user_repository() -> IUserRepository:
    return user_repository
