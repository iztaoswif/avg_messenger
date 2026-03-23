from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.users import (
    insert_user,
    select_user_by_username,
    is_username_taken
)
from redis.asyncio import Redis
from app.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from app.core.passwords import get_password_hash, is_password_correct
from app.core.token import create_access_token
from app.core.rate_limit import is_rate_limited
from app.core.exceptions import RateLimitedError


async def register_user(
    session: AsyncSession,
    redis_client: Redis,
    username: str,
    password: str) -> None:

    if is_rate_limited(redis_client, f"register_username:{username}"):
        raise RateLimitedError

    is_username_taken_result = await is_username_taken(session, username)
    if is_username_taken_result:
        raise UsernameTakenError()

    password_hash = await get_password_hash(password)
    await insert_user(session, username, password_hash)


async def login_user(
    session: AsyncSession,
    redis_client: Redis,
    username: str,
    password: str) -> str:

    if is_rate_limited(redis_client, f"login_username:{username}"):
        raise RateLimitedError

    user = await select_user_by_username(session, username)
    if user is None:
        raise InvalidCredentialsError()

    is_password_correct_result = await is_password_correct(user["password_hash"], password)
    if not is_password_correct_result:
        raise InvalidCredentialsError()

    token = create_access_token({"sub": str(user["id"])})
    return token
