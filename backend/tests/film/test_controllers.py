import pytest
from httpx import AsyncClient


class TestFilmController:
    @pytest.mark.asyncio
    async def test_get_films(self, client: AsyncClient) -> None:
        response = await client.get(url="/films/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
