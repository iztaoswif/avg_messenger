from pydantic import BaseModel, field_validator
from app.core.config import MAX_TEXT_LENGTH
from app.chat.exceptions import (
    InappropriateMessageTextError,
    InappropriateChatIdError
)
from typing import List


def validate_message_text(text: str) -> str:
    if len(text) == 0:
        raise InappropriateMessageTextError("Text must be at least 1 character long")

    text = text.strip()

    if len(text) > MAX_TEXT_LENGTH:
        raise InappropriateMessageTextError(f"Text must be at most {MAX_TEXT_LENGTH} characters long")

    if len(text) == 0:
        raise InappropriateMessageTextError("Text has no printable characters")

    for char in text:
        if not (32 <= ord(char) <= 126 or 1040 <= ord(char) <= 1103):
            raise InappropriateMessageTextError("Illegal characters in the message")

    return text


class SendTextMessageRequest(BaseModel):
    chat_id: int
    content: str

    @field_validator("chat_id")
    @classmethod
    def validate_chat_id(cls, chat_id: int) -> int:
        if chat_id < 1:
            raise InappropriateChatIdError

        return chat_id

    @field_validator("content")
    @classmethod
    def validate_content(cls, content: str) -> str:
        content = validate_message_text(content)
        return content


class SendTextMessageResponse(BaseModel):
    message: str


class ResponseMessage(BaseModel):
    id: int
    sender_id: int
    sender_username: str
    content: str
    created_at: str


class GetMessagesResponse(BaseModel):
    messages: List[ResponseMessage]
