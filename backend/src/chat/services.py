from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.exc import IntegrityError
from core.dto import Message
from core.exceptions import ForbiddenError
from chat.exceptions import (
    ChatNotFoundError
)
from auth.exceptions import UserNotFoundError
from repositories.messages import (
    select_messages_after,
    insert_message
)
from repositories.chats import (
    insert_chat,
    select_chat
)
from repositories.chat_members import (
    insert_chat_member
)
from chat.exceptions import AlreadyChatMemberError
from core.helper_types import ChatId, MessageId, UserId

#TODO
# raise ChatNotFoundError()
# raise ForbiddenError()


async def fetch_messages(
    conn: AsyncConnection,
    chat_id: ChatId,
    after_id: MessageId | None
) -> list[Message]:
    messages = await select_messages_after(conn, chat_id, after_id)
    return messages


async def add_member_to_chat(
    conn: AsyncConnection,
    chat_id: ChatId,
    user_id: UserId
) -> None:
    try:
        await insert_chat_member(conn, chat_id, user_id)

    except IntegrityError as e:
        await conn.rollback()
        print(e)
        raise NotImplementedError()


async def add_new_chat(
    conn: AsyncConnection,
    name: str,
    creator_id: UserId
) -> ChatId:
    try:
        new_chat_id = await insert_chat(conn, name, creator_id)
    
    # ONLY TIME FOREIGN KEY CONSTRAINT CAN BE VIOLATED IS IF CREATOR DOES NOT ACTUALLY EXISTS
    except IntegrityError:
        raise UserNotFoundError()
    return new_chat_id


async def create_message_in_chat(
    conn: AsyncConnection,
    sender_id: UserId,
    chat_id: ChatId,
    content: str
) -> None:
    await insert_message(
        conn,
        sender_id,
        chat_id,
        content
    )


async def fetch_chat_name(
    conn: AsyncConnection,
    id: ChatId
) -> str:
    chat = await select_chat(conn, id)

    if chat is None:
        raise ChatNotFoundError()

    return chat.name
