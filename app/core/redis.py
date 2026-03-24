from redis.asyncio import Redis
import os
from dotenv import load_dotenv
load_dotenv()


def create_redis_client() -> Redis:
    host = os.getenv("REDIS_HOST")
    port = int(os.getenv("REDIS_PORT"))
    db = int(os.getenv("REDIS_DB"))

    return Redis(
        host=host,
        port=port,
        db=db,
        decode_responses=True,
        max_connections=30
    )
