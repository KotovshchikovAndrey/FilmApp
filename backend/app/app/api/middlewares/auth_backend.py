import typing as tp

from starlette.authentication import AuthenticationBackend, AuthCredentials, BaseUser


class JwtUser(BaseUser):
    def __init__(self) -> None:
        super().__init__()
