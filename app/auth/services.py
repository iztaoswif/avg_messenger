from app.repositories.users import (create_user,
get_user_by_username,
is_username_taken)

from app.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from app.core.passwords import hash_password, is_password_correct
from app.core.token import create_access_token


def register_user(username: str, password: str) -> None:
    if is_username_taken(username):
        raise UsernameTakenError()

    password_hash = hash_password(password)
    create_user(username, password_hash)


def login_user(username: str, password: str) -> str:
    user = get_user_by_username(username)

    if user is None or not is_password_correct(password, user["password_hash"]):
        raise InvalidCredentialsError()

    token = create_access_token({"sub": str(user["id"])})
    return token
