from redis.asyncio import Redis
import os

def create_redis_client() -> Redis:
    return Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True,
        max_connections=30
    )
