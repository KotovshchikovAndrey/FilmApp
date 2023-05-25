import typing as tp

import jwt
from starlette.authentication import AuthCredentials, AuthenticationBackend, BaseUser
from starlette.requests import HTTPConnection

from app.core import config
from app.exceptions.api import ApiError
from user.crud.reporitories.user import get_user_repository
from user.dto.user import UserBase


class JwtUser(BaseUser):
    def __init__(self, instance: UserBase, token: str) -> None:
        self.instance = instance
        self.token = token

    @property
    def is_authenticated(self) -> bool:
        return True

    def __str__(self) -> int:
        return self.instance.id


def parse_token(conn: HTTPConnection, header_name: str = "authorization") -> str:
    token = conn.headers.get(header_name, None)
    if token is None:
        raise ApiError.unauthorized(message="Token was not provided")
    return token


def decode_token(token: str) -> tp.Dict[str, tp.Any]:
    payload = jwt.decode(jwt=token, key=str(config.SECRET_KEY), algorithms=["HS256"])
    return payload


class JwtAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        if "Authorization" not in conn.headers:
            return
        token = parse_token(conn)
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise ApiError.unauthorized(message="The token has expired")
        except jwt.InvalidTokenError:
            raise ApiError.unauthorized(message="Wrong token")
        current_user = await get_user_repository().find_by_id(target_id=payload["id"])
        if current_user is None:
            raise ApiError.not_found(message="User not found")
        user_status = current_user["status"]
        if user_status == "banned":
            raise ApiError.forbidden("Your account has been banned")
        credentials = ["authenticated"]
        if user_status == "active":
            credentials.append("active")
        if current_user["role"] == "admin":
            credentials.append("admin")
        return (
            AuthCredentials(credentials),
            JwtUser(instance=UserBase(**current_user), token=token),
        )
