from sqlalchemy import (
    insert,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection
from auth.exceptions import UsernameTakenError
from core.dto import User
from core.helper_types import UserId
from core.passwords import is_password_correct
from db.models import users


async def insert_user(
    conn: AsyncConnection,
    username: str,
    password_hash: str
) -> UserId:
    stmt = (
        insert(users)
        .values(
            username=username,
            password_hash=password_hash
        )
        .returning(users.c.id)
    )
    try:
        result = await conn.execute(stmt)
    except IntegrityError:
        raise UsernameTakenError

    return result.scalar_one()


async def select_user(
    conn: AsyncConnection,
    id: UserId
) -> User | None:
    stmt = (
        select(users)
        .where(users.c.id == id)
    )

    result = await conn.execute(stmt)
    user_row = result.mappings().first()

    if user_row is None: return None

    return User(
        id=user_row.id,
        username=user_row.username
    )


async def select_user_id_by_credentials(
    conn: AsyncConnection,
    username: str,
    password: str
) -> UserId | None:
    stmt = (
        select(users)
        .where(users.c.username == username)
    )

    result = await conn.execute(stmt)
    user_row = result.mappings().first()

    if user_row is None: return None
    if not is_password_correct(user_row.password_hash, password): return None

    return user_row.id
