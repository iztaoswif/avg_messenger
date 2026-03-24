from sqlalchemy import (
    insert,
    select,
    exists
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import chats, chat_members
from typing import List, Dict, Optional


async def insert_chat(
    session: AsyncSession,
    name: str) -> int:

    stmt = insert(chats).values(name=name).returning(chats.c.id)
    result = await session.execute(stmt)
    return result.scalar_one()


async def select_chats_by_user_id(
    session: AsyncSession,
    user_id: int) -> List[Dict]:

    stmt = (
        select(
            chats.c.id,
            chats.c.name
        )
        .join(chat_members, chats.c.id == chat_members.c.chat_id)
        .where(chat_members.c.user_id == user_id)
        .order_by(chats.c.id.asc())
    )

    result = await session.execute(stmt)
    return [
        {
            "id": row.id,
            "name": row.name
        }
        for row in result.mappings()
    ]


async def select_chat_name_by_id(
    session: AsyncSession,
    id: int) -> Optional[str]:

    stmt = stmt = select(chats.c.name).where(chats.c.id == id)

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def is_chat_exists(
    session: AsyncSession,
    chat_id: int) -> bool:

    stmt = select(exists().where(chats.c.id == chat_id))

    result = await session.execute(stmt)
    return result.scalar()


async def is_chat_id_exists(
    session: AsyncSession,
    id: int) -> bool:

    stmt = select(exists().where(chats.c.id == id))

    result = await session.execute(stmt)
    return result.scalar()
