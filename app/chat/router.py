from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_asyncsession
from app.chat.schemas import (
    SendTextMessageRequest,
    SendTextMessageResponse,
    GetMessagesResponse)

from app.auth.dependencies import get_current_user_id
from app.repositories.messages import (
    create_message_in_db
)
from app.chat.services import fetch_messages

chat_router = APIRouter(prefix="/chat",
tags=["Chat"])


@chat_router.post("/send")
async def send(
    request: SendTextMessageRequest,
    sender_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_asyncsession)) -> SendTextMessageResponse:

    chat_id, content = request.chat_id, request.content

    await create_message_in_db(session, sender_id, chat_id, content)

    return SendTextMessageResponse(message="Message sent successfully")


@chat_router.get("/messages")
async def get_messages(
    chat_id: int,
    after_id: int = 0,
    session: AsyncSession = Depends(get_asyncsession)) -> GetMessagesResponse:

    messages = await fetch_messages(session, chat_id, after_id)

    return GetMessagesResponse(messages=messages)
