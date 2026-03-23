from typing import AsyncGenerator
from app.core.redis import create_redis_client
from redis.asyncio import Redis

async def get_redis() -> AsyncGenerator[Redis, None]:
    redis_client = create_redis_client()
    try:
        yield redis_client
    finally:
        await redis_client.aclose()