from redis.asyncio import Redis


async def is_rate_limited(
    redis_client: Redis,
    user_id: int,
    limit: int = 5,
    window_seconds: int = 1) -> bool:

    rate_limiter_key = f"rate_limit:{user_id}"

    current = await redis_client.get(rate_limiter_key)

    if current is None:
        redis_client.set(rate_limiter_key, 1, ex=window_seconds)
        return True

    if int(current) > limit:
        return False

    redis_client.incr(rate_limiter_key)
    return True
