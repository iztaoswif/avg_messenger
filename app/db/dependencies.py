from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.engine import engine
from app.main import redis_client
from redis.asyncio import Redis

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_asyncsession() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_redis() -> AsyncGenerator[Redis, None]:
    yield redis_client
