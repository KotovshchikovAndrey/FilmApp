# Если ты решил почитать этот код, то ты весьма отчаянный)
# Все это говно нужно переписывать и рефакторить!


import pytest
from httpx import AsyncClient
from datetime import date

from app.core.ioc import container, film_services
from film.dto import (
    GetFilmsDTO,
    CreateFilmDTO,
    UpdateFilmDTO,
    SetFilmRatingDTO,
    ResetFilmRaitingDTO,
)

IFilmService = film_services.IFilmService


class TestFilmService:
    @pytest.mark.parametrize(
        "input_value, output_value",
        (
            (GetFilmsDTO(limit=10), 10),
            (GetFilmsDTO(limit=5), 5),
            (GetFilmsDTO(limit=10, offset=10), 10),
        ),
    )
    async def test_get_films_assortment_limit(
        self, client: AsyncClient, input_value, output_value
    ) -> None:
        service: IFilmService = container.resolve(IFilmService)

        films = await service.get_films_assortment(input_value)
        assert len(films.films) == output_value

    @pytest.mark.parametrize(
        "input_value, output_value",
        (
            (
                GetFilmsDTO(limit=1, genre="Animation"),
                {"Animation"},
            ),
            (
                GetFilmsDTO(limit=1, genre="Comedy", country="US"),
                {"Comedy", "US"},
            ),
            (
                GetFilmsDTO(limit=1, country="US"),
                {"US"},
            ),
        ),
    )
    async def test_get_films_assortment_filters(
        self, client: AsyncClient, input_value, output_value
    ) -> None:
        service: IFilmService = container.resolve(IFilmService)

        films = await service.get_films_assortment(input_value)
        film = films.films[0]
        response = await client.get(url=f"/films/{film.id}")
        film = response.json()

        genres_values = [genre["name"] for genre in film["genres"]]
        countries_values = [
            country["iso_3166_1"] for country in film["production_countries"]
        ]

        assert output_value.issubset(set(genres_values).union(countries_values)) == True

    @pytest.mark.parametrize(
        "input_value",
        (
            CreateFilmDTO(
                title="Test",
                is_adult=True,
                description="Test desc",
                imdb_id="tt12345678",
                language="EN",
                budget=100,
                release_date=date(year=2023, month=8, day=10),
                genres=[{"name": "test"}],
                production_companies=[],
                production_countries=[],
                tagline=None,
                time=1.5,
            ),
        ),
    )
    async def test_create_new_film(self, client: AsyncClient, input_value) -> None:
        service: IFilmService = container.resolve(IFilmService)

        film_id = await service.create_new_film(input_value)
        film = await service.get_film_info(film_id)

        assert film.title == input_value.title
        assert film.description == input_value.description
        assert film.budget == input_value.budget
        assert film.tagline == input_value.tagline
        assert str(film.production_companies) == input_value.production_companies
        assert str(film.production_countries) == input_value.production_countries

    @pytest.mark.parametrize(
        "input_value",
        (
            (
                1,
                UpdateFilmDTO(title="Test", is_adult=True, budget=150),
            ),
        ),
    )
    async def test_update_film_info(self, client: AsyncClient, input_value) -> None:
        service: IFilmService = container.resolve(IFilmService)

        film_before_update = await service.get_film_info(input_value[0])
        film_id = await service.update_film_info(*input_value)
        film_after_update = await service.get_film_info(film_id)

        assert film_after_update.title == input_value[-1].title
        assert film_after_update.is_adult == input_value[-1].is_adult
        assert film_after_update.budget == input_value[-1].budget

        assert film_after_update.description == film_before_update.description
        assert film_after_update.genres == film_before_update.genres
        assert film_after_update.language == film_before_update.language

    @pytest.mark.asyncio
    async def test_film_rating(self, client: AsyncClient, test_users) -> None:
        service: IFilmService = container.resolve(IFilmService)

        test_case = (
            (
                SetFilmRatingDTO(user=test_users[0], film_id=1, value=5),
                SetFilmRatingDTO(user=test_users[1], film_id=1, value=3),
                SetFilmRatingDTO(user=test_users[2], film_id=1, value=2),
                SetFilmRatingDTO(user=test_users[3], film_id=1, value=1),
            ),
            2.75,
            2,
        )

        set_ratings, avg_rating, avg_rating_before_reset = test_case
        for rating in set_ratings:
            await service.set_film_rating(rating)

        avg_film_rating = await service.calculate_film_rating(film_id=1)
        assert avg_film_rating.rating == avg_rating

        dto = ResetFilmRaitingDTO(user=test_users[0], film_id=1)
        await service.reset_film_rating(dto)

        film_rating_before_reset = await service.calculate_film_rating(film_id=1)
        assert film_rating_before_reset.rating == avg_rating_before_reset

    @pytest.mark.asyncio
    async def test_empty_film_rating(self, client: AsyncClient) -> None:
        service: IFilmService = container.resolve(IFilmService)

        film_id = 2
        film_raiting = await service.calculate_film_rating(film_id=film_id)

        assert film_raiting.rating == 0
        assert film_raiting.film_id == film_id
