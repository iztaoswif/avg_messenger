from pydantic import BaseModel, field_validator

from app.core.config import MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH
from app.auth.exceptions import InappropriateUsernameError, InappropriatePasswordError
import re


class MessageResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def validate_username(username: str) -> str:
    if username == "":
        raise InappropriateUsernameError("Username must be at least 1 character long")

    username = username.strip()

    if username == "":
        raise InappropriateUsernameError("Username must not be empty")

    if len(username) > MAX_USERNAME_LENGTH:
        raise InappropriateUsernameError(f"Username must be at most {MAX_USERNAME_LENGTH} characters long")

    zw_regex = re.compile(r'[\u200b-\u200d\u2060\ufeff]')
    if bool(zw_regex.search(username)):
        raise InappropriateUsernameError("Invalid characters in the username")

    return username


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise InappropriatePasswordError("Password must be at least 8 characters long")

    if len(password) > MAX_PASSWORD_LENGTH:
        raise InappropriatePasswordError(f"Password must be at most {MAX_PASSWORD_LENGTH} characters long")

    for char in password:
        if not 32 <= ord(char) <= 126:
            raise InappropriatePasswordError("Invalid characters in password")

    return password


class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username_register(cls, username: str) -> str:
        username = validate_username(username)
        return username

    @field_validator("password")
    @classmethod
    def validate_password_register(cls, password: str) -> str:
        password = validate_password(password)
        return password


class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username_login(cls, username: str) -> str:
        username = validate_username(username)
        return username

    @field_validator("password")
    @classmethod
    def validate_password_login(cls,password: str) -> str:
        password = validate_password(password)
        return password


class GetMeResponse(BaseModel):
    user_id: int
