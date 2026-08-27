from sqlalchemy import (
    insert,
    select,
)
from sqlalchemy.ext.asyncio import AsyncConnection
from core.dto import Message
from core.helper_types import ChatId, MessageId, UserId
from db.models import messages


async def insert_message(
    conn: AsyncConnection,
    sender_id: UserId,
    chat_id: ChatId,
    content: str
) -> MessageId:
    stmt = (
        insert(messages)
        .values(
            chat_id=chat_id,
            sender_id=sender_id,
            content=content
        )
        .returning(messages.c.id)
    )
    result = await conn.execute(stmt)
    return result.scalar_one()


async def select_messages_after(
    conn: AsyncConnection,
    chat_id: ChatId,
    after_id: MessageId | None
) -> list[Message]:
    base_stmt = (
        select(
            messages.c.id,
            messages.c.sender_id,
            messages.c.content,
            messages.c.created_at,
        )
        .where(messages.c.chat_id == chat_id)
        .order_by(messages.c.created_at.asc())
    )

    result = await conn.execute(base_stmt)
    return [
        Message(
            id=row.id,
            sender_id=row.sender_id,
            content=row.content,
            created_at=row.created_at
        )

        for row in result.mappings()
    ]
