from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.chat.exceptions import (
    InappropriateChatIdError,
    InappropriateIdError
)
from app.repositories.messages import (
    select_messages
)
from app.repositories.chats import (
    is_chat_exists,
    is_chat_id_exists
)
from app.repositories.chat_members import insert_chat_member
from app.chat.exceptions import AlreadyChatMemberError


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
