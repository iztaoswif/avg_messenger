from fastapi import APIRouter, Depends

from app.chat.schemas import (SendTextMessageRequest,
SendTextMessageResponse)

from app.auth.dependencies import get_current_user_id

from app.repositories.messages import (fetch_messages,
create_message)

chat_router = APIRouter(prefix="/chat",
tags=["Chat"])


@chat_router.post("/send")
def send(
        request: SendTextMessageRequest,
        sender_id: int = Depends(get_current_user_id)
    ) -> SendTextMessageResponse:
    content = request.content
    create_message(sender_id, content)
    return SendTextMessageResponse(message="Message sent successfully")


@chat_router.get("/messages")
def get_messages(after_id: int = 0):
    return fetch_messages(after_id)
