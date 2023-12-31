from concurrent.futures import ThreadPoolExecutor
import typing as tp
import asyncio
from abc import ABC, abstractmethod

from app.core import config
from app.exceptions.api import ApiError

# from app.utils.ai_models.smart_search import search_films
from app.utils.file_manager import FileManager
from film.crud.reporitories import IFilmReporitory
from film.services import imdb, ICommentService

from user.dto import UserBase
from film.dto import (
    CreateFilmDTO,
    FilmDTO,
    FilmFiltersDTO,
    FilmRatingDTO,
    FilmsDTO,
    FilmTrailerDTO,
    GetFilmsDTO,
    GetPosterDTO,
    SearchFilmDTO,
    SetFilmRatingDTO,
    UpdateFilmDTO,
    ResetFilmRaitingDTO,
    AddCommentDTO,
    UpdateCommentDTO,
    FilmCommentsDTO,
    UserFilmInfoDTO,
    RequestUserFilmInfo,
    GigaSearchFilmDTO,
)


class IFilmService(ABC):
    __repository: IFilmReporitory
    __comment_service: ICommentService

    @abstractmethod
    async def get_films_assortment(self, dto: GetFilmsDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_info(self, film_id: int) -> FilmDTO:
        ...

    @abstractmethod
    async def get_users_film_info(self, dto: RequestUserFilmInfo) -> UserFilmInfoDTO:
        ...

    @abstractmethod
    async def search_film(self, dto: SearchFilmDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def giga_search_film(self, dto: GigaSearchFilmDTO) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_film_filters(self) -> FilmFiltersDTO:
        ...

    @abstractmethod
    async def get_poster_for_film(self, dto: GetPosterDTO) -> tp.Tuple[bytes, bool]:
        ...

    @abstractmethod
    async def get_trailer_for_film(self, film_id: int) -> FilmTrailerDTO:
        ...

    @abstractmethod
    async def create_new_film(self, dto: CreateFilmDTO) -> int:
        ...

    @abstractmethod
    async def update_film_info(
        self, film_id: int, dto: UpdateFilmDTO
    ) -> tp.Optional[int]:
        ...

    @abstractmethod
    async def delete_film(self, film_id: int) -> tp.Optional[int]:
        ...

    @abstractmethod
    async def get_user_favorite_films(self, target_id: int, order_by: str) -> FilmsDTO:
        ...

    @abstractmethod
    async def get_user_watch_status_films(
        self, target_id: int, status: str, order_by: str
    ) -> FilmsDTO:
        ...

    @abstractmethod
    async def calculate_film_rating(self, film_id: int) -> FilmRatingDTO:
        ...

    @abstractmethod
    async def set_film_rating(self, dto: SetFilmRatingDTO) -> None:
        ...

    @abstractmethod
    async def reset_film_rating(self, dto: ResetFilmRaitingDTO) -> None:
        ...

    @abstractmethod
    async def get_film_comments(self, film_id: int) -> FilmCommentsDTO:
        ...

    @abstractmethod
    async def add_comment_to_film(self, dto: AddCommentDTO) -> int:
        ...

    @abstractmethod
    async def update_film_comment(self, dto: UpdateCommentDTO) -> int:
        ...

    @abstractmethod
    async def delete_film_comment(self, comment_id: int, user: UserBase) -> int:
        ...


class FilmService(IFilmService):
    def __init__(self, repository: IFilmReporitory, comment_service: ICommentService):
        self.__repository = repository
        self.__comment_service = comment_service

    async def get_films_assortment(self, dto: GetFilmsDTO):
        films = await self.__repository.get_many(
            limit=dto.limit,
            offset=dto.offset,
            genre=dto.genre,
            country=dto.country,
        )

        return films

    async def get_film_info(self, film_id: int):
        film = await self.__repository.find_by_id(film_id)
        if film is None:
            raise ApiError.not_found(message="Film not found!")

        return film

    async def get_users_film_info(self, dto: RequestUserFilmInfo) -> UserFilmInfoDTO:
        collection_info = await self.__repository.get_users_film_info(
            dto.user_id, dto.film_id
        )
        return collection_info

    async def get_film_filters(self) -> FilmFiltersDTO:
        film_genres = await self.__repository.get_all_genres()
        film_countries = await self.__repository.get_all_production_countries()

        return FilmFiltersDTO(genres=film_genres, countries=film_countries)

    async def get_poster_for_film(self, dto: GetPosterDTO):
        film = await self.__repository.find_by_id(dto.film_id)
        if film is None:
            raise ApiError.not_found(message="Film not found!")

        imdb_id = film.imdb_id
        if imdb_id is not None:
            poster_url = await imdb.fetch_poster_url_by_imdb_id(imdb_id)
            if poster_url is not None:
                poster = await imdb.fetch_poster_binary_file(poster_url, dto.size)
                return poster, True

        file_manager = FileManager(upload_dir=config.UPLOAD_DIR + "/posters")
        poster = await file_manager.read("default_poster.jpg")

        return poster, False

    async def get_trailer_for_film(self, film_id: int):
        film = await self.__repository.find_by_id(film_id)
        if film is None:
            raise ApiError.not_found(message="Film not found!")

        imdb_id = film.imdb_id
        if imdb_id is not None:
            trailer_url = await imdb.fetch_trailer_url_by_imdb_id(imdb_id)
            if trailer_url is not None:
                return trailer_url

        return FilmTrailerDTO(key="dQw4w9WgXcQ", site="YouTube")  # пасхалка :D

    async def search_film(self, dto: SearchFilmDTO):
        films = await self.__repository.find_by_title(title=dto.title, limit=dto.limit)
        return films

    async def giga_search_film(self, dto: GigaSearchFilmDTO):
        with ThreadPoolExecutor(max_workers=4) as pool:
            event_loop = asyncio.get_running_loop()
        #     film_id = await event_loop.run_in_executor(pool, search_films, dto.title)

        # film = await self.__repository.find_by_id(film_id)
        # return FilmsDTO(films=[film])

    async def create_new_film(self, dto: CreateFilmDTO):
        created_film = await self.__repository.create(dto)
        return created_film.id

    async def update_film_info(self, film_id: int, dto: UpdateFilmDTO):
        updated_film = await self.__repository.update(film_id, dto)
        if updated_film is not None:
            return updated_film.id

    async def delete_film(self, film_id: int):
        deleted_film = await self.__repository.delete(film_id)
        if deleted_film is not None:
            return deleted_film.id

    async def get_user_favorite_films(self, target_id: int, order_by: str):
        films = await self.__repository.get_favorite_films(target_id, order_by)
        return films

    async def get_user_watch_status_films(
        self, target_id: int, status: str, order_by: str
    ):
        films = await self.__repository.get_watch_status_films(
            target_id, status, order_by
        )
        return films

    async def calculate_film_rating(self, film_id: int):
        film_rating = await self.__repository.aggregate_rating(film_id)
        if film_rating is not None:
            rating = film_rating.rating
            film_rating.rating = round(rating, 2)
            return film_rating

        return FilmRatingDTO(rating=0, film_id=film_id)

    async def set_film_rating(self, dto: SetFilmRatingDTO):
        return await self.__repository.set_rating(
            user_id=dto.user.id, film_id=dto.film_id, value=dto.value
        )

    async def reset_film_rating(self, dto: ResetFilmRaitingDTO):
        return await self.__repository.reset_rating(
            user_id=dto.user.id, film_id=dto.film_id
        )

    async def get_film_comments(self, film_id: int):
        comments = await self.__comment_service.get_film_comments(film_id)
        film_comments = FilmCommentsDTO(comments=comments)

        return film_comments

    async def add_comment_to_film(self, dto: AddCommentDTO):
        if dto.parent_comment is not None:
            comment = await self.__comment_service.find_comment_by_id(
                comment_id=dto.parent_comment
            )

            if comment is None:
                raise ApiError.not_found(message="Parent comment does not exists!")

            # Максимальная вложенность комментариев друг в друга - 1
            # ( У комментария есть вложенные комментарии,
            # но у вложенных комментариев нет вложенности )
            if comment.parent_comment is not None:
                raise ApiError.bad_request(message="Maximum nesting exceeded!")

        new_comment = await self.__comment_service.create_film_comment(dto)
        return new_comment.comment_id

    async def update_film_comment(self, dto: UpdateCommentDTO):
        comment_in_db = await self.__comment_service.find_comment_by_id(dto.comment_id)
        if comment_in_db is None:
            raise ApiError.not_found(message="Comment not found!")

        # Пользователь может редактировать только свои комментарии
        if comment_in_db.user_id != dto.user.id:
            raise ApiError.forbidden(message="Forbidden to update!")

        updated_comment = await self.__comment_service.update_film_comment(
            comment_id=dto.comment_id,
            new_text=dto.text,
        )

        return updated_comment.comment_id

    async def delete_film_comment(self, comment_id: int, user: UserBase):
        comment_in_db = await self.__comment_service.find_comment_by_id(comment_id)
        if comment_in_db is None:
            raise ApiError.not_found(message="Comment does not exists!")

        # Пользователь может удалять только свои комментарии
        if comment_in_db.user_id != user.id:
            raise ApiError.forbidden(message="Forbidden to delete!")

        deleted_comment = await self.__comment_service.delete_film_comment(comment_id)
        return deleted_comment.comment_id
