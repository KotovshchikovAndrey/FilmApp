import typing as tp
from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: str
    avatar: tp.Optional[str] = None
    user_role: str
    user_status: str


class GetUsersDTO(BaseModel):
    email: str


class UsersDTO(BaseModel):
    user: tp.List[UserBase]
