from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

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
    session: AsyncSession = Depends(get_asyncsession)) -> MessageResponse:

    username, password = request.username, request.password

    await register_user(session, username, password)

    return MessageResponse(message="Successful register")


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_asyncsession)) -> TokenResponse:

    username, password = form.username, form.password

    token = await login_user(session, username, password)

    return TokenResponse(access_token=token)
