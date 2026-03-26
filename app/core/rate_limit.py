from redis.asyncio import Redis


async def is_rate_limited(
    redis_client: Redis,
    key_identifier: str,
    limit: int = 5,
    window_seconds: int = 1) -> bool:

    key = f"rate_limit:{key_identifier}"

    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.incr(key)
        pipe.expire(key, window_seconds)
        results = await pipe.execute()
        current_count = results[0]

    return current_count > limit
