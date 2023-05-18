from pydantic import BaseModel

from user.dto import UserBase


class UserRefreshTokenDTO(BaseModel):
    user: UserBase
    access_token: str
    refresh_token: str


class UserLogoutDTO(BaseModel):
    user: UserBase
    refresh_token: str
