import pytest
from httpx import AsyncClient
from datetime import date

from app.core.ioc import container, film_services
from app.utils.fakers import user_faker
from film.dto import GetFilmsDTO, CreateFilmDTO, UpdateFilmDTO, SetFilmRatingDTO

IFilmService = film_services.IFilmService


class TestFilmService:
    @pytest.mark.asyncio
    async def test_get_films_assortment_limit(self, client: AsyncClient) -> None:
        service: IFilmService = container.resolve(IFilmService)

        test_cases = (
            (GetFilmsDTO(limit=10), 10),
            (GetFilmsDTO(limit=5), 5),
            (GetFilmsDTO(limit=10, offset=10), 10),
        )

        for input_value, output_value in test_cases:
            films = await service.get_films_assortment(input_value)
            assert len(films.films) == output_value

    @pytest.mark.asyncio
    async def test_get_films_assortment_filters(self, client: AsyncClient) -> None:
        service: IFilmService = container.resolve(IFilmService)

        test_cases = (
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
        )

        for input_value, output_value in test_cases:
            films = await service.get_films_assortment(input_value)
            film = films.films[0]
            response = await client.get(url=f"/films/{film.id}")
            film = response.json()

            genres_values = [genre["name"] for genre in film["genres"]]
            countries_values = [
                country["iso_3166_1"] for country in film["production_countries"]
            ]

            assert (
                output_value.issubset(set(genres_values).union(countries_values))
                == True
            )

    @pytest.mark.asyncio
    async def test_create_new_film(self, client: AsyncClient) -> None:
        service: IFilmService = container.resolve(IFilmService)

        test_cases = (
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
        )

        for input_value in test_cases:
            film_id = await service.create_new_film(input_value)
            film = await service.get_film_info(film_id)

            assert film.title == input_value.title
            assert film.description == input_value.description
            assert film.budget == input_value.budget
            assert film.tagline == input_value.tagline
            assert str(film.production_companies) == input_value.production_companies
            assert str(film.production_countries) == input_value.production_countries

    @pytest.mark.asyncio
    async def test_update_film_info(self, client: AsyncClient) -> None:
        service: IFilmService = container.resolve(IFilmService)

        test_cases = ((1, UpdateFilmDTO(title="Test", is_adult=True, budget=150)),)

        for input_value in test_cases:
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
    async def test_film_raiting(self, client: AsyncClient) -> None:
        service: IFilmService = container.resolve(IFilmService)

        fake_users = await user_faker.create_fake_users(count=4)
        test_cases = (
            (
                (
                    SetFilmRatingDTO(user=fake_users[0], film_id=1, value=5),
                    SetFilmRatingDTO(user=fake_users[1], film_id=1, value=3),
                    SetFilmRatingDTO(user=fake_users[2], film_id=1, value=2),
                    SetFilmRatingDTO(user=fake_users[3], film_id=1, value=1),
                ),
                2.75,
            ),
        )

        for case in test_cases:
            set_raitings, avg_raiting = case
            for raiting in set_raitings:
                await service.set_film_rating(raiting)

            avg_film_raiting = await service.calculate_film_rating(film_id=1)
            assert avg_film_raiting.rating == avg_raiting
