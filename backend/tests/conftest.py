import os
import typing as tp

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from src.app.utils.commands import drop_tables, run_migrations


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
            transport=ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://127.0.0.1:8000",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
