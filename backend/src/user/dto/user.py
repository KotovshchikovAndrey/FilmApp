import datetime
import enum
import typing as tp

from pydantic import BaseModel, Json, validator

from app.exceptions.api import ApiError
from app.utils.OtherUtils import email_validate


class UserBase(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    avatar: tp.Optional[str] = None
    status: str
    role: str
    is_public: bool


class UserPublicDTO(BaseModel):
    id: int
    name: str
    surname: str
    avatar: tp.Optional[str] = None


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
    reason: tp.Literal[
        "complete-register", "change-email", "reset-password"
    ] = "UNKNOWN REASON"


class UserChangingEmailDTO(UserRequestCodeDTO):
    new_email: str


class UserLoginDTO(BaseModel):
    email: str
    password: str


class GetUserWatchStatusFilmsDTO(BaseModel):
    class OrderUserFilmsEnum(str, enum.Enum):
        id = "id"
        date = "updated_date"

    user: UserBase
    watch_status: tp.Literal[
        "not_watching",
        "watching",
        "in_plans",
        "scheduled",
        "watched",
        "postponed",
        "abandoned",
    ] = "watching"
    order_by: OrderUserFilmsEnum = OrderUserFilmsEnum.date


class ManageWatchStatusFilmDTO(BaseModel):
    user_id: int
    film_id: int
    watch_status: tp.Literal[
        "not_watching",
        "watching",
        "in_plans",
        "scheduled",
        "watched",
        "postponed",
        "abandoned",
    ]


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
    def validate_file(cls, value: str):
        if not value:
            raise ValueError("Avatar file was not sent!")

        return value

    @validator("filename")
    def validate_filename(cls, value: str):
        allowed_ext = {"png", "jpg", "jpeg", "gif"}
        ext = value.split(".")[-1]

        if ext not in allowed_ext:
            print(ext)
            raise ValueError(
                f"Unsupported extension! Available: {allowed_ext}"
            )

        return value

    @validator("content")
    def validate_filesize(cls, value: bytes):
        if len(value) > 10485760:
            raise ApiError.file_too_large(
                message="The file size should not exceed 10MB."
            )
        return value


class UserAvatarDTO(BaseModel):
    avatar_url: str


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

    @validator("new_password")
    def validate_length(cls, value: str):
        if not 8 <= len(value) <= 100:
            raise ValueError("Password length must be between 8 and 100 characters")
        return value


class UserChangeEmail(BaseModel):
    user: UserBase
    new_email: str

    @validator("new_email")
    def validate_length(cls, value: str):
        if len(value) > 50:
            raise ValueError("Email length must not exceed 50 characters")
        if not email_validate(value):
            raise ValueError("Invalid email address")
        return value


class UserRequestResetPasswordDTO(BaseModel):
    email: str


class UserResetPasswordDTO(BaseModel):
    token: str
    password: str
