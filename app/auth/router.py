from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schemas import (MessageResponse,
TokenResponse,
RegisterRequest)

from app.auth.services import register_user, login_user


auth_router = APIRouter(prefix="/auth",
tags=["Auth"])


@auth_router.post("/register")
def register(request: RegisterRequest) -> MessageResponse:
    username, password = request.username, request.password
    register_user(username, password)
    login_user(username, password)
    return MessageResponse(message="successful register")


@auth_router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    token = login_user(form.username, form.password)
    return TokenResponse(access_token=token)
