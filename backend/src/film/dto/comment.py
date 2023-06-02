from __future__ import annotations

import typing as tp
from pydantic import BaseModel, validator

from user.dto import UserBase


class CommentPrimaryKeyDTO(BaseModel):
    comment_id: int


class CommentAuthorDTO(BaseModel):
    name: str
    surname: str
    avatar: tp.Optional[str]


class BaseCommentDTO(CommentPrimaryKeyDTO):
    text: str
    author: CommentAuthorDTO


class CommentDTO(BaseCommentDTO):
    child_comments: tp.List[BaseCommentDTO] = []


class FilmCommentsDTO(BaseModel):
    comments: tp.List[CommentDTO] = []


class CommentInDB(BaseModel):
    id: int
    user_id: int
    film_id: int
    text: str
    parent_comment: tp.Optional[int] = None


class AddCommentDTO(BaseModel):
    user: UserBase
    film_id: int
    text: str
    parent_comment: tp.Optional[int]

    @validator("text")
    def validate_text(cls, value: str):
        if len(value) == 0:
            raise ValueError("Comment text should not be empty!")

        return value


class UpdateCommentDTO(BaseModel):
    user: UserBase
    text: str
    comment_id: int

    @validator("text")
    def validate_text(cls, value: str):
        if len(value) == 0:
            raise ValueError("Comment text should not be empty!")

        return value
