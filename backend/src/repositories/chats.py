from sqlalchemy import (
    insert,
    select
)
from sqlalchemy.ext.asyncio import AsyncConnection
from core.dto import Chat
from core.helper_types import ChatId, UserId
from db.models import chats, chat_members


async def insert_chat(
    conn: AsyncConnection,
    name: str,
    creator_id: UserId
) -> ChatId:
    stmt = (
        insert(chats)
        .values(
            name=name,
            creator_id=creator_id
        )
        .returning(chats.c.id))
    result = await conn.execute(stmt)
    return result.scalar_one()


async def select_chats_of_user(
    conn: AsyncConnection,
    user_id: UserId
) -> list[Chat]:
    stmt = (
        select(
            chats.c.id,
            chats.c.name
        )
        .join(chat_members, chats.c.id == chat_members.c.chat_id)
        .where(chat_members.c.user_id == user_id)
        .order_by(chats.c.id.asc())
    )

    result = await conn.execute(stmt)

    return [
        Chat(
            id=row.id,
            name=row.name
        )
        for row in result.mappings()
    ]


async def select_chat(
    conn: AsyncConnection,
    id: ChatId
) -> Chat | None:
    stmt = (
        select(chats.c.name)
        .where(chats.c.id == id)
    )

    name = (await conn.execute(stmt)).scalar_one_or_none()

    if name is None: return None

    return Chat(
        id=id,
        name=name
    )
