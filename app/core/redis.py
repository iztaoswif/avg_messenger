from redis.asyncio import Redis, from_url
import os
from dotenv import load_dotenv
load_dotenv()


def create_redis_client() -> Redis:
    redis_url = os.getenv("REDIS_URL")

    return from_url(
        redis_url,
        decode_responses=True,
        max_connections=30
    )
