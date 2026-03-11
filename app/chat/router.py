from fastapi import APIRouter, Depends

from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_asyncsession
from app.chat.schemas import (
    SendTextMessageRequest,
    SendTextMessageResponse,
    GetMessagesResponse)

from app.auth.dependencies import get_current_user_id
from app.repositories.messages import (fetch_messages,
create_message)

chat_router = APIRouter(prefix="/chat",
tags=["Chat"])


@chat_router.post("/send")
async def send(
    request: SendTextMessageRequest,
    sender_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_asyncsession)) -> SendTextMessageResponse:

    content = request.content

    await create_message(session, sender_id, content)

    return SendTextMessageResponse(message="Message sent successfully")


@chat_router.get("/messages")
async def get_messages(
    after_id: int = 0,
    session: AsyncSession = Depends(get_asyncsession)) -> List[Dict]:

    messages = await fetch_messages(session, after_id)

    return GetMessagesResponse(messages=messages)
