from sqlalchemy import (
    insert,
    select,
    exists
)

from app.chat.exceptions import AlreadyChatMemberError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import chat_members


async def insert_chat_member(
    session: AsyncSession,
    chat_id: int,
    user_id: int) -> None:

    try:
        stmt = insert(chat_members).values(
            chat_id=chat_id,
            user_id=user_id
        )

        await session.execute(stmt)
    
    except IntegrityError:
        raise AlreadyChatMemberError()


async def is_chat_member(
    session: AsyncSession,
    chat_id: int,
    user_id: int) -> bool:

    stmt = select(exists()
    .where(chat_members.c.chat_id == chat_id)
    .where(chat_members.c.user_id == user_id))

    result = await session.execute(stmt)
    return result.scalar()
