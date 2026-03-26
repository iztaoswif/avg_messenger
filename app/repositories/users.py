from sqlalchemy import (insert,
select,
exists)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import RowMapping

from typing import Optional
from app.db.models import users


async def is_username_taken(
    session: AsyncSession,
    username: str) -> bool:

    stmt = select(exists().where(users.c.username == username))

    result = await session.execute(stmt)
    return result.scalar()


async def insert_user(
    session: AsyncSession,
    username: str,
    password_hash: str) -> int:

    stmt = insert(users).values(
        username=username,
        password_hash=password_hash
    ).returning(users.c.id)

    id = await session.execute(stmt)
    return id.scalar()


async def select_user_by_username(
    session: AsyncSession,
    username: str) -> Optional[RowMapping]:

    stmt = select(users).where(users.c.username == username).limit(1)

    result = await session.execute(stmt)
    return result.mappings().first()


async def select_user_by_id(
    session: AsyncSession,
    id: int) -> Optional[RowMapping]:

    stmt = select(users).where(users.c.id == id).limit(1)

    result = await session.execute(stmt)
    return result.mappings().first()
