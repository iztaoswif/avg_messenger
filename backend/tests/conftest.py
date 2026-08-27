import pytest
import sqlite3
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from db.models import chats
from sqlalchemy import insert
from main import app
from db.models import metadata
from db.dependencies import get_async_connection

TEST_DATABASE_URL = "sqlite+aiosqlite:///tests/test.db"

test_engine = create_async_engine(TEST_DATABASE_URL)


@pytest.fixture(autouse=True)
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
async def client(conn: AsyncConnection):
    async def override_get_async_connection():
        yield conn

    app.dependency_overrides[get_async_connection] = override_get_async_connection

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
