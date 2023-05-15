import datetime
import typing as tp
from pydantic import BaseModel, Json


# Токены и коды восстановления не должны быть здесь - небезопасно
class UserBase(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    avatar: tp.Optional[str] = None
    status: str
    role: str


class UserFullDTO(UserBase):
    password: str
    refresh_tokens: tp.List[str] = []
    reset_codes: Json[tp.Any]


class UserRegisterDTO(BaseModel):
    name: str
    surname: str
    email: str
    password: str


class UserVerificationData(BaseModel):
    ip: str
    code: str
    email: str
    timestamp: datetime.datetime = datetime.datetime.now()
