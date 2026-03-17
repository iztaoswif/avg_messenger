from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.exceptions import (
    InappropriateChatIdError,
    InappropriateIdError
)
from app.repositories.messages import (
    is_chat_exists,
    is_id_exists,
    get_messages_from_db
)


async def fetch_messages(
    session: AsyncSession,
    chat_id: int,
    after_id: int = 0):

    if not await is_chat_exists(session, chat_id):
        raise InappropriateChatIdError()

    if not await is_id_exists(session, chat_id):
        raise InappropriateIdError()

    messages = await get_messages_from_db(session, chat_id, after_id)
    return messages
