from sqlalchemy import (
    insert,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from app.db.models import messages, users


async def insert_message(
    session: AsyncSession,
    sender_id: int,
    chat_id: int,
    content: str) -> None:

    stmt = insert(messages).values(
        chat_id=chat_id,
        sender_id=sender_id,
        content=content
    )

    await session.execute(stmt)
    await session.commit()


async def select_messages(
    session: AsyncSession,
    chat_id: int,
    after_id: int) -> List[Dict]:

    stmt = (
        select(
            messages.c.id,
            messages.c.sender_id,
            messages.c.content,
            messages.c.created_at,
            users.c.username.label("sender_username")
        )
        .join(users, messages.c.sender_id == users.c.id)
        .where(messages.c.chat_id == chat_id)
        .where(messages.c.id > after_id)
        .order_by(messages.c.id.asc())
    )

    result = await session.execute(stmt)
    return [
        {
            "id": row.id,
            "sender_id": row.sender_id,
            "sender_username": row.sender_username,
            "content": row.content,
            "created_at": row.created_at.isoformat()
        }

        for row in result.mappings()
    ]
