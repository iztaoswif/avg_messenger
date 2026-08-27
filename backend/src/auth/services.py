from sqlalchemy.ext.asyncio import AsyncConnection
from repositories.users import (
    insert_user,
    select_user_id_by_credentials
)
from auth.exceptions import InvalidCredentialsError
from core.passwords import calculate_password_hash
from core.token import create_access_token


async def register_user(
    conn: AsyncConnection,
    username: str,
    password: str
) -> None:
    password_hash = await calculate_password_hash(password)
    new_user_id = await insert_user(conn, username, password_hash)


async def login_user(
    conn: AsyncConnection,
    username: str,
    password: str
) -> str:
    user_id = await select_user_id_by_credentials(conn, username, password)
    if user_id is None:
        raise InvalidCredentialsError()

    token = create_access_token({"sub": str(user_id)})
    return token
