from pydantic import BaseModel

from user.dto import UserBase


class UserRefreshTokenDTO(BaseModel):
    user: UserBase
    access_token: str
    refresh_token: str
