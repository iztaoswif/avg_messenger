from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncConnection
from core.helper_types import UserId
from db.dependencies import get_async_connection
from auth.schemas import (
    MessageResponse,
    TokenResponse,
    RegisterRequest,
    GetMeResponse
)

from auth.services import register_user, login_user
from auth.dependencies import get_current_user_id


auth_router = APIRouter(prefix="/auth",
tags=["Auth"])


@auth_router.post("/register")
async def register(
    request: RegisterRequest,
    conn: AsyncConnection = Depends(get_async_connection),
) -> MessageResponse:
    await register_user(conn, request.username, request.password)

    return MessageResponse(message="Successful register")


@auth_router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    conn: AsyncConnection = Depends(get_async_connection),
) -> TokenResponse:
    token = await login_user(conn, form.username, form.password)

    return TokenResponse(access_token=token)


@auth_router.get("/me")
async def me(
    user_id: UserId = Depends(get_current_user_id)
) -> GetMeResponse:
    return GetMeResponse(user_id=user_id)
