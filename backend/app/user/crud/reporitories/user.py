import typing as tp
from abc import ABC, abstractmethod

from app.utils.OtherUtils import get_password_hash
from user.dto import UserRegisterDTO, UserVerificationData, UserLoginDTO
from app.db import db_connection
from user.crud import queries


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
    async def verify_user(self, id: int) -> tp.Mapping:
        ...

    @abstractmethod
    async def authorise_user(self, dto: UserLoginDTO) -> tp.Mapping:
        ...

    @abstractmethod
    async def add_verification_code(self, dto: UserVerificationData) -> tp.Mapping:
        ...

    @abstractmethod
    async def find_by_id(self, target_id: int) -> tp.Mapping:
        ...

    @abstractmethod
    async def update(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def add_to_favorite(self, user_id: int, film_id: int):
        ...

    @abstractmethod
    async def add_refresh_token(self, user_id: int, refresh_token: str):
        ...

    @abstractmethod
    async def replace_refresh_token(self, target_id: int, old_token: str, new_token: str):
        ...

    @abstractmethod
    async def check_refresh_token(self, target_id: int, refresh_token: str) -> bool:
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
            queries.FIND_USER_BY_EMAIL,
            email=dto.email
        )
        return user

    async def find_by_email(self, email: str):
        user = await db_connection.fetch_one(
            queries.FIND_USER_BY_EMAIL,
            email=email
        )
        return user

    async def find_by_email_and_code(self, email: str, code: str):
        user = await db_connection.fetch_one(
            queries.FIND_USER_WITH_CODE,
            email=email,
            code=code
        )
        return user

    async def find_by_id(self, target_id: int):
        user = await db_connection.fetch_one(
            queries.FIND_USER_BY_ID,
            id=target_id
        )
        return user

    async def verify_user(self, id: int):
        await db_connection.execute_query(
            queries.VERIFY_USER,
            id=id,
        )
        user = await self.find_by_id(id)
        return user

    async def authorise_user(self, dto: UserLoginDTO):
        user = await db_connection.fetch_one(
            queries.AUTHORISE_USER,
            email=dto.email,
            password=get_password_hash(dto.password)
        )
        return user

    # Этот костыль здесь не просто так. По-другому запрос отказывался выполняться.
    # Если есть непреодолимое желание исправить это, удачи. Мне лень.
    async def add_verification_code(self, dto: UserVerificationData):
        await db_connection.execute_query(
            queries.ADD_NEW_VERIFICATION_CODE.replace('PASTE_JSON_HERE',
                                                      "'{\"ip\": \"" + dto.ip + "\", \"code\": \"" + dto.code + "\", \"timestamp\": " + str(
                                                          int(dto.timestamp)) + ", \"reason\": \"" + dto.reason + "\"}'"),
            email=dto.email
        )

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int):
        ...

    async def add_to_favorite(self, user_id: int, film_id: int):
        ...

    async def add_refresh_token(self, user_id: int, refresh_token: str):
        await db_connection.execute_query(
            queries.ADD_REFRESH_TOKEN,
            refresh_token=refresh_token,
            id=user_id,
        )

    async def replace_refresh_token(self, target_id: int, old_token: str, new_token: str):
        await db_connection.execute_query(
            queries.UPDATE_REFRESH_TOKEN,
            old_token=old_token,
            new_token=new_token,
            target_id=target_id
        )

    async def check_refresh_token(self, target_id: int, refresh_token: str) -> bool:
        user = await db_connection.fetch_one(
            queries.CHECK_REFRESH_TOKEN,
            target_id=target_id,
            refresh_token=refresh_token
        )
        return user is not None


user_repository = UserPostgresRepository()


def get_user_repository() -> IUserRepository:
    return user_repository
