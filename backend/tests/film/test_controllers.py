import pytest
from httpx import AsyncClient


class TestFilmController:
    @pytest.mark.asyncio
    async def test_get_films(self, client: AsyncClient) -> None:
        response = await client.get(url="/films/", params={"limit": 10})
        assert response.status_code == 200
        films = response.json()["films"]
        assert len(films) == 10

        must_return_fields = ("id", "title", "is_adult", "tagline")
        assert tuple(films[0].keys()) == must_return_fields

    @pytest.mark.asyncio
    async def test_film_detail(self, client: AsyncClient) -> None:
        response = await client.get(url="/films/1")
        assert response.status_code == 200

        film = response.json()
        must_return_fields = (
            "id",
            "title",
            "is_adult",
            "description",
            "language",
            "budget",
            "release_date",
            "time",
            "genres",
            "production_companies",
            "production_countries",
        )

        assert tuple(film.keys()) == must_return_fields

    @pytest.mark.asyncio
    async def test_film_not_exists(self, client: AsyncClient) -> None:
        response = await client.get(url="/films/0")
        assert response.status_code == 404
        assert response.json()["message"] == "Film not found!"

    @pytest.mark.asyncio
    async def test_filter_films(self, client: AsyncClient) -> None:
        filter_params = {
            "limit": 5,
            "genre": "Crime",
            "country": "US",
        }

        response = await client.get(url="/films/", params=filter_params)
        assert response.status_code == 200

        film = response.json()["films"][0]

        film_id = film["id"]
        response = await client.get(url=f"/films/{film_id}")

        film_detail = response.json()

        film_detail_genres_names = [genre["name"] for genre in film_detail["genres"]]
        film_detail_countries_names = [
            country["iso_3166_1"] for country in film_detail["production_countries"]
        ]

        assert filter_params["genre"] in film_detail_genres_names
        assert filter_params["country"] in film_detail_countries_names

    @pytest.mark.asyncio
    async def test_create_film_correct(self, client: AsyncClient) -> None:
        data = {
            "title": "TEST",
            "is_adult": True,
            "description": "TEST",
            "language": "en",
            "budget": 30000000,
            "release_date": "1995-10-30",
            "time": 81.0,
            "genres": [
                {"id": 16, "name": "Animation"},
                {"id": 35, "name": "Comedy"},
                {"id": 10751, "name": "Family"},
            ],
            "production_companies": [{"id": 3, "name": "Pixar Animation Studios"}],
        }

        response = await client.post(url="/films/", json=data)
        assert response.status_code == 201

        created_film_id = int(response.json())
        response = await client.get(url=f"/films/{created_film_id}")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_film_incorrect(self, client: AsyncClient) -> None:
        invalid_fields_in_data = {
            "is_adult",
            "release_date",
            "genres",
            "time",
            "title",
            "production_companies",
            "production_countries",
        }

        data = {
            "title": "",
            "is_adult": "INCORRECT BOOL VALUE",
            "description": "TEST",
            "language": "en",
            "budget": 30000000,
            "release_date": "199510-30",
            "time": -100,
            "genres": [{"incorrect_field": "TEST"}],
            "production_companies": "null",
            "production_countries": "null",
        }

        response = await client.post(url="/films/", json=data)
        assert response.status_code == 400

        invalid_fields = []
        for field in response.json()["details"]:
            invalid_fields.extend(field["loc"])

        assert invalid_fields_in_data.issubset(set(invalid_fields)) == True

    @pytest.mark.asyncio
    async def test_update_film_incorrect(self, client: AsyncClient) -> None:
        invalid_fields_in_data = {
            "production_companies",
            "production_countries",
        }

        response = await client.get(url="/films/1")
        data = dict(response.json())

        data["production_companies"] = {"": ""}
        data["production_countries"] = [{"": ""}]

        response = await client.patch(url="/films/1", json=data)
        assert response.status_code == 400

        invalid_fields = []
        for field in response.json()["details"]:
            invalid_fields.extend(field["loc"])

        assert invalid_fields_in_data.issubset(set(invalid_fields)) == True

    @pytest.mark.asyncio
    async def test_update_film_correct(self, client: AsyncClient) -> None:
        response = await client.get(url="/films/1")
        data_before_update = dict(response.json())

        data_before_update["genres"] = [{"name": "Test Genre"}]
        data_before_update["production_companies"] = []
        data_before_update["production_countries"] = [
            {
                "name": "Test Name1",
                "iso_3166_1": "Test Iso",
            },
            {
                "name": "Test Name2",
                "iso_3166_1": "Test Iso",
            },
        ]

        response = await client.patch(url="/films/1", json=data_before_update)
        assert response.status_code == 200

        response = await client.get(url="/films/1")
        data_after_update = response.json()

        assert data_after_update["genres"] == data_before_update["genres"]
        assert (
            data_after_update["production_countries"]
            == data_before_update["production_countries"]
        )
        assert (
            data_after_update["production_companies"]
            == data_before_update["production_companies"]
        )
