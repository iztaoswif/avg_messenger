from sqlalchemy import (
    insert,
    select,
    exists
)

from chat.exceptions import AlreadyChatMemberError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection
from core.helper_types import ChatId, UserId
from db.models import chat_members


async def insert_chat_member(
    conn: AsyncConnection,
    chat_id: ChatId,
    user_id: UserId
) -> None:
    stmt = (
        insert(chat_members)
        .values(
            chat_id=chat_id,
            user_id=user_id
        )
    )

    try:
        await conn.execute(stmt)
    #TODO: ANALYZE WHAT ARE THE POSSIBLE ERRORS HERE
    except IntegrityError as e:
        print(e)
