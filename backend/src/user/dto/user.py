import datetime
import enum
import typing as tp

from pydantic import BaseModel, Json, validator


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


class UserRequestCodeDTO(BaseModel):
    code: str
    email: str
    timestamp: int = int(datetime.datetime.now().timestamp())
    reason: tp.Literal["complete-register", "change-email"] = "UNKNOWN REASON"


class UserChangingEmailDTO(UserRequestCodeDTO):
    new_email: str


class UserLoginDTO(BaseModel):
    email: str
    password: str


class AddFavoriteFilmDTO(BaseModel):
    user: UserBase
    film_id: int


class GetUserFavoriteFilmsDTO(BaseModel):
    class OrderUserFilmsEnum(str, enum.Enum):
        id = "id"
        date = "added_date"

    user: UserBase
    order_by: OrderUserFilmsEnum = OrderUserFilmsEnum.id


class ManageFavoriteFilmDTO(BaseModel):
    user_id: int
    film_id: int


class FileDTO(BaseModel):
    filename: str
    content: bytes

    @validator("filename", "content")
    def validate_filename(cls, value: str):
        if not value:
            raise ValueError("Avatar file was not sent!")

        return value


class UserAvatarDTO(BaseModel):
    avatar_url: str

    @validator("avatar_url", pre=True)
    def validate_avatar_url(cls, value: str):
        return f"/{value}"


class UpdateProfileDTO(BaseModel):
    name: str
    surname: str

    @validator("name", "surname")
    def validate_length(cls, value: str):
        if len(value) > 30:
            raise ValueError("The field must not exceed 30 characters!")

        return value


class UserChangePassword(BaseModel):
    user: UserBase
    old_password: str
    new_password: str
