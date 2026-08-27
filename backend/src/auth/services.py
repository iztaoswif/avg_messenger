from sqlalchemy.ext.asyncio import AsyncSession
from repositories.users import (
    insert_user,
    select_user_by_username,
    is_username_taken
)
from repositories.chat_members import insert_chat_member
from auth.exceptions import UsernameTakenError, InvalidCredentialsError
from core.passwords import get_password_hash, is_password_correct
from core.token import create_access_token


async def register_user(
    session: AsyncSession,
    username: str,
    password: str
) -> None:
    if await is_username_taken(session, username):
        raise UsernameTakenError()

    ORIGIN_CHAT_ID = 1
    password_hash = await get_password_hash(password)
    new_user_id = await insert_user(session, username, password_hash)
    await insert_chat_member(session, ORIGIN_CHAT_ID, new_user_id)


async def login_user(
    session: AsyncSession,
    username: str,
    password: str
) -> str:
    user = await select_user_by_username(session, username)
    if user is None:
        raise InvalidCredentialsError()

    if not await is_password_correct(user["password_hash"], password):
        raise InvalidCredentialsError()

    token = create_access_token({"sub": str(user["id"])})
    return token
