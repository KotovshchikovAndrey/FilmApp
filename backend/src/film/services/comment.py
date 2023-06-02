import typing as tp
from abc import ABC, abstractmethod

from user.dto import UserBase
from film.dto import AddCommentDTO, UpdateCommentDTO
from film.crud.reporitories import ICommentRepository

from film.dto import AddCommentDTO, CommentPrimaryKeyDTO, CommentDTO, CommentInDB


class ICommentService(ABC):
    __repository: ICommentRepository

    @abstractmethod
    async def find_comment_by_id(self, comment_id: int) -> tp.Optional[CommentInDB]:
        ...

    @abstractmethod
    async def get_film_comments(self, film_id: int) -> tp.List[CommentDTO]:
        ...

    @abstractmethod
    async def create_film_comment(self, dto: AddCommentDTO) -> CommentPrimaryKeyDTO:
        ...

    @abstractmethod
    async def update_film_comment(
        self, comment_id: int, new_text: str
    ) -> CommentPrimaryKeyDTO:
        ...

    @abstractmethod
    async def delete_film_comment(self, comment_id: int) -> CommentPrimaryKeyDTO:
        ...


class CommentService(ICommentService):
    def __init__(self, repository: ICommentRepository) -> None:
        self.__repository = repository

    async def find_comment_by_id(self, comment_id: int):
        comment = await self.__repository.find_by_id(comment_id)
        return comment

    async def get_film_comments(self, film_id: int):
        comments = await self.__repository.get_all_parents(film_id)
        for comment in comments:
            child_comments = await self.__repository.get_all_childen(comment.comment_id)
            comment.child_comments = child_comments

        return comments

    async def create_film_comment(self, dto: AddCommentDTO):
        return await self.__repository.create(
            film_id=dto.film_id,
            user_id=dto.user.id,
            text=dto.text,
            parent_comment=dto.parent_comment,
        )

    async def update_film_comment(
        self, comment_id: int, new_text: str
    ) -> CommentPrimaryKeyDTO:
        return await self.__repository.update(comment_id=comment_id, text=new_text)

    async def delete_film_comment(self, comment_id: int):
        deleted_comment = await self.__repository.delete(comment_id)
        return deleted_comment
