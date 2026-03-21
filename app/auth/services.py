from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.users import (insert_user,
select_user_by_username,
is_username_taken)

from app.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from app.core.passwords import get_password_hash, is_password_correct
from app.core.token import create_access_token


async def register_user(
    session: AsyncSession,
    username: str,
    password: str) -> None:

    is_username_taken_result = await is_username_taken(session, username)
    if is_username_taken_result:
        raise UsernameTakenError()

    password_hash = await get_password_hash(password)
    await insert_user(session, username, password_hash)


async def login_user(
    session: AsyncSession,
    username: str,
    password: str) -> str:

    user = await select_user_by_username(session, username)
    if user is None:
        raise InvalidCredentialsError()

    is_password_correct_result = await is_password_correct(user["password_hash"], password)
    if not is_password_correct_result:
        raise InvalidCredentialsError()

    token = create_access_token({"sub": str(user["id"])})
    return token
