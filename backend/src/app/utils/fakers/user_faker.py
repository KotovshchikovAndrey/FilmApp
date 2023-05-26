import typing as tp

from app.core.ioc import user_services, container
from user.dto import UserRegisterDTO, UserBase

IUserService = user_services.IUserService

service: IUserService = container.resolve(IUserService)


async def create_fake_users(count: int = 1) -> tp.List[UserBase]:
    data: tp.Dict[str, str] = {
        "name": "TestName_{}",
        "surname": "TestSurname_{}",
        "email": "ykt_testuser_{}@mail.com",
        "password": "12345678",
    }

    users = []
    for index in range(count):
        name = data["name"].format(index)
        surname = data["surname"].format(index)
        email = data["email"].format(index)
        password = data["password"]

        dto = UserRegisterDTO(
            name=name,
            surname=surname,
            email=email,
            password=password,
        )

        user = await service.create_user(dto)
        users.append(user)

    return users
