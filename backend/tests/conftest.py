import typing as tp

import os
import pytest

from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from src.app.utils.commands import run_migrations, drop_tables


@pytest.fixture(scope="session")
def prepare_database():
    os.environ["IS_TESTING"] = "True"
    run_migrations()
    yield
    drop_tables()


@pytest.fixture
async def client(prepare_database: None) -> AsyncClient:
    from src.main import app

    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://127.0.0.1:8000",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
