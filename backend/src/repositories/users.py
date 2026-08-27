from sqlalchemy import (
    insert,
    select,
    exists
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.dto import User
from core.helper_types import UserId
from db.models import users


# JUST FOR UX PURPOSES
async def is_username_taken(
    session: AsyncSession,
    username: str
) -> bool:
    stmt = (
        select(
            exists()
            .where(users.c.username == username)
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one()


async def insert_user(
    session: AsyncSession,
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

    result = await session.execute(stmt)
    return result.scalar_one()


async def select_user(
    session: AsyncSession,
    id: UserId
) -> User | None:
    stmt = (
        select(users)
        .where(users.c.id == id)
    )

    result = await session.execute(stmt)
    user_row = result.mappings().first()

    if user_row is None: return None

    return User(
        id=user_row.id,
        username=user_row.username
    )
