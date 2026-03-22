import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.db.models import metadata
from app.db.dependencies import get_asyncsession

TEST_DATABASE_URL = "sqlite+aiosqlite:///tests/test.db"

test_engine = create_async_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
async def create_delete_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture
async def session(create_delete_tables):
    async with test_engine.connect() as conn:
        await conn.begin()

        async with AsyncSession(bind=conn) as s:
            yield s
            await conn.rollback()


@pytest.fixture
async def client(session):
    async def override_get_asyncsession():
        yield session

    app.dependency_overrides[get_asyncsession] = override_get_asyncsession
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
