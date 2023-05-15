import typing as tp
from abc import ABC, abstractmethod
from user.dto import UserBase, UserRegisterDTO, UserVerificationData
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
    async def verify_user(self, id: int) -> None:
        ...

    @abstractmethod
    async def add_verification_code(self, dto: UserVerificationData) -> tp.Mapping:
        ...

    @abstractmethod
    async def find_by_id(self, id: int) -> tp.Mapping:
        ...

    @abstractmethod
    async def update(self, **kwargs: ...) -> ...:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def add_to_favorite(self, user_id: int, car_id: int):
        ...


class UserPostgresRepository(IUserRepository):
    async def create(self, dto: UserRegisterDTO):
        await db_connection.execute_query(
            queries.CREATE_NEW_USER,
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            password=dto.password
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

    # Этот костыль здесь не просто так. По-другому запрос отказывался выполняться.
    # Если есть непреодолимое желание исправить это, удачи. Мне лень.
    async def add_verification_code(self, dto: UserVerificationData):
        await db_connection.execute_query(
            queries.ADD_NEW_VERIFICATION_CODE.replace('PASTE_JSON_HERE',
                                                      "'{\"ip\": \"" + dto.ip + "\", \"code\": \"" + dto.code + "\", \"timestamp\": \"" + str(
                                                          dto.timestamp) + "\"}'"),
            email=dto.email
        )

    async def update(self, **kwargs: ...):
        ...

    async def delete(self, user_id: int):
        ...

    async def add_to_favorite(self, user_id: int, car_id: int):
        ...
