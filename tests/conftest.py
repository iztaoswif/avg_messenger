import pytest
import sqlite3
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fakeredis.aioredis import FakeRedis

from app.main import app
from app.db.models import metadata
from app.db.dependencies import get_asyncsession
from app.core.dependencies import get_redis

TEST_DATABASE_URL = "sqlite+aiosqlite:///tests/test.db"

test_engine = create_async_engine(TEST_DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
async def create_delete_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture
async def db_connection():
    async with test_engine.connect() as conn:
        await conn.begin()
        
        raw_conn = await conn.get_raw_connection()
        raw_conn.driver_connection.row_factory = sqlite3.Row
        
        yield conn
        
        await conn.rollback()


@pytest.fixture
async def session(db_connection):
    async with AsyncSession(bind=db_connection, expire_on_commit=False) as s:
        yield s


@pytest.fixture
async def sqlite_connection(db_connection):
    raw_conn = await db_connection.get_raw_connection()
    return raw_conn.driver_connection


@pytest.fixture
async def redis():
    async with FakeRedis(decode_responses=True) as r:
        yield r


@pytest.fixture
async def client(session, redis):
    async def override_get_asyncsession():
        yield session

    async def override_get_redis():
        yield redis

    app.dependency_overrides[get_asyncsession] = override_get_asyncsession
    app.dependency_overrides[get_redis] = override_get_redis

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
