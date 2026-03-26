from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ForbiddenError
from app.chat.exceptions import (
    InappropriateChatIdError,
    ChatNotFoundError
)
from app.repositories.messages import (
    select_messages,
    insert_message
)
from app.repositories.chats import (
    insert_chat,
    is_chat_exists,
    select_chat_name_by_id
)
from app.repositories.chat_members import (
    insert_chat_member,
    is_chat_member
)
from app.chat.exceptions import AlreadyChatMemberError


async def ensure_chat_access(
    session: AsyncSession,
    chat_id: int,
    user_id: int) -> None:

    if not await is_chat_exists(session, chat_id):
        raise ChatNotFoundError()

    if not await is_chat_member(session, chat_id, user_id):
        raise ForbiddenError()


async def fetch_messages(
    session: AsyncSession,
    chat_id: int,
    user_id: int,
    after_id: int = 0):

    messages = await select_messages(session, chat_id, after_id)
    return messages


async def add_member_to_chat(
    session: AsyncSession,
    chat_id: int,
    user_id: int) -> None:

    try:
        await insert_chat_member(session, chat_id, user_id)

    except IntegrityError:
        await session.rollback()
        raise AlreadyChatMemberError()


async def add_new_chat(
    session: AsyncSession,
    name: str,
    creator_id: int) -> int:

    new_chat_id = await insert_chat(session, name)
    await insert_chat_member(session, new_chat_id, creator_id)

    return new_chat_id


async def create_message_in_chat(
    session: AsyncSession,
    redis_client: Redis,
    sender_id: int,
    chat_id: int,
    content: str) -> None:

    await insert_message(
        session,
        sender_id,
        chat_id,
        content
    )


async def fetch_chat_name_by_id(
    session: AsyncSession,
    id: int) -> str:

    chat_name = await select_chat_name_by_id(session, id)

    if chat_name is None:
        raise ChatNotFoundError()

    return chat_name
