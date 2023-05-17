import typing as tp

import jwt
from app.exceptions.api import ApiError
from user.dto.user import UserBase
from app.core import config
from user.crud.reporitories.user import get_user_repository
from starlette.requests import HTTPConnection
from starlette.authentication import AuthenticationBackend, AuthCredentials, BaseUser


class JwtUser(BaseUser):
    def __init__(self, usr: UserBase, token: str) -> None:
        self.usr = usr
        self.token = token

    @property
    def is_authenticated(self) -> bool:
        return True

    def __str__(self) -> int:
        return self.usr.id


def parse_token(conn: HTTPConnection) -> str:
    token = conn.headers.get("authorization", None)
    if token is None:
        raise ApiError.unauthorized(message="Token was not provided")
    return token


def decode_token(token: str) -> tp.Dict[str, tp.Any]:
    payload = jwt.decode(jwt=token, key=config.SECRET_KEY, algorithms=["HS256"])
    return payload


class JwtAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        if "Authorization" not in conn.headers:
            return
        token = parse_token(conn)
        try:
            payload = decode_token(token)
        except jwt.InvalidTokenError:
            raise ApiError.forbidden(message="Wrong token")
        current_user = await get_user_repository().find_by_id(id=payload["id"])
        if current_user is None:
            raise ApiError.not_found(message="User not found")
        return (
            AuthCredentials(["authenticated"]),
            JwtUser(usr=UserBase(**current_user), token=token),
        )
