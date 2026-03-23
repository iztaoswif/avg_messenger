from redis.asyncio import Redis


async def is_rate_limited(
    redis_client: Redis,
    key_identifier: str,
    limit: int = 5,
    window_seconds: int = 1) -> bool:

    key = "rate_limit:" + key_identifier

    current = await redis_client.incr(key)

    if current == 1:
        await redis_client.expire(key, window_seconds)

    return current > limit
