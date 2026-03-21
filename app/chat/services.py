from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.chat.exceptions import (
    InappropriateChatIdError,
    InappropriateIdError
)
from app.repositories.messages import (
    select_messages,
    insert_message
)
from app.repositories.chats import (
    is_chat_exists,
    is_chat_id_exists
)
from app.repositories.chat_members import insert_chat_member
from app.chat.exceptions import AlreadyChatMemberError
from app.core.exceptions import RateLimitedError
from app.core.rate_limit import is_rate_limited


async def fetch_messages(
    session: AsyncSession,
    chat_id: int,
    after_id: int = 0):

    if not await is_chat_exists(session, chat_id):
        raise InappropriateChatIdError()

    if not await is_chat_id_exists(session, chat_id):
        raise InappropriateIdError()

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


async def create_new_message(
    session: AsyncSession,
    redis_client: Redis,
    sender_id: int,
    chat_id: int,
    content: str) -> None:

    if await is_rate_limited(redis_client, sender_id):
        raise RateLimitedError()

    await insert_message(
        session,
        sender_id,
        chat_id,
        content
    )
