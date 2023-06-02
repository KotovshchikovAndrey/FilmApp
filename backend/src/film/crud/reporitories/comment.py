import typing as tp
from abc import ABC, abstractmethod

from app.db import db_connection

from film.crud import queries
from film.dto import (
    CommentPrimaryKeyDTO,
    CommentDTO,
    CommentAuthorDTO,
    BaseCommentDTO,
    CommentInDB,
)


class ICommentRepository(ABC):
    @abstractmethod
    async def find_by_id(self, comment_id: int) -> tp.Optional[CommentInDB]:
        ...

    @abstractmethod
    async def get_all_parents(self, film_id: int) -> tp.List[CommentDTO]:
        ...

    @abstractmethod
    async def get_all_childen(self, comment_id: int) -> tp.List[BaseCommentDTO]:
        ...

    @abstractmethod
    async def create(
        self,
        film_id: int,
        user_id: int,
        text: str,
        parent_comment: tp.Optional[int] = None,
    ) -> CommentPrimaryKeyDTO:
        ...

    @abstractmethod
    async def update(self, comment_id: int, text: str) -> CommentPrimaryKeyDTO:
        ...

    @abstractmethod
    async def delete(self, comment_id: int) -> CommentPrimaryKeyDTO:
        ...


class CommentPostgresRepository(ICommentRepository):
    async def find_by_id(self, comment_id: int):
        comment = await db_connection.fetch_one(
            queries.GET_COMMENT_BY_ID, comment_id=comment_id
        )

        if comment is not None:
            return CommentInDB(**comment)

    async def get_all_parents(self, film_id: int):
        comments = await db_connection.fetch_all(
            queries.GET_ALL_PARENT_COMMENTS_FOR_FILM, film_id=film_id
        )

        comments_list = []
        for comment in comments:
            author = CommentAuthorDTO(**comment)
            comment = CommentDTO(**comment, author=author)
            comments_list.append(comment)

        return comments_list

    async def get_all_childen(self, comment_id: int):
        comments = await db_connection.fetch_all(
            queries.GET_ALL_CHILD_COMMENTS_FOR_COMMENT, comment_id=comment_id
        )

        comments_list = []
        for comment in comments:
            author = CommentAuthorDTO(**comment)
            comment = BaseCommentDTO(**comment, author=author)
            comments_list.append(comment)

        return comments_list

    async def create(
        self,
        film_id: int,
        user_id: int,
        text: str,
        parent_comment: tp.Optional[int] = None,
    ):
        new_comment = await db_connection.fetch_one(
            queries.CREATE_FILM_COMMENT,
            user_id=user_id,
            film_id=film_id,
            text=text,
            parent_comment=parent_comment,
        )

        return CommentPrimaryKeyDTO(**new_comment)

    async def update(self, comment_id: int, text: str):
        updated_comment = await db_connection.fetch_one(
            queries.UPDATE_FILM_COMMENT, comment_id=comment_id, text=text
        )

        return CommentPrimaryKeyDTO(**updated_comment)

    async def delete(self, comment_id: int):
        deleted_comment = await db_connection.fetch_one(
            queries.DELETE_FILM_COMMENT,
            comment_id=comment_id,
        )

        return CommentPrimaryKeyDTO(**deleted_comment)
