from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.exceptions import RateLimitedError
from app.core.dependencies import get_redis
from app.core.rate_limit import is_rate_limited
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_asyncsession
from app.auth.schemas import (MessageResponse,
TokenResponse,
RegisterRequest)

from app.auth.services import register_user, login_user


auth_router = APIRouter(prefix="/auth",
tags=["Auth"])


@auth_router.post("/register")
async def register(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_asyncsession),
    redis_client: Redis = Depends(get_redis)) -> MessageResponse:

    username, password = request.username, request.password

    if is_rate_limited(redis_client, f"register_username:{username}"):
        raise RateLimitedError

    await register_user(session, username, password)

    await session.commit()

    return MessageResponse(message="Successful register")


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_asyncsession),
    redis_client: Redis = Depends(get_redis)) -> TokenResponse:

    username, password = form.username, form.password

    if is_rate_limited(redis_client, f"login_username:{username}"):
        raise RateLimitedError

    token = await login_user(session, username, password)

    return TokenResponse(access_token=token)
