from pydantic import BaseModel, field_validator, Field
from app.core.config import (
    MAX_TEXT_LENGTH,
    MAX_CHAT_NAME_LENGTH
)
from app.chat.exceptions import (
    InappropriateMessageTextError,
    InappropriateChatNameError
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
    chat_id: int = Field(ge=1)
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, content: str) -> str:
        content = validate_message_text(content)
        return content


class ResponseMessage(BaseModel):
    id: int = Field(ge=1)
    sender_id: int = Field(ge=1)
    sender_username: str
    content: str
    created_at: str


class GetMessagesResponse(BaseModel):
    messages: List[ResponseMessage]


def validate_chat_name(chat_name: str) -> str:
    if len(chat_name) == 0:
        raise InappropriateChatNameError("Text must be at least 1 character long")

    chat_name = chat_name.strip()

    if len(chat_name) > MAX_CHAT_NAME_LENGTH:
        raise InappropriateChatNameError(f"Chat name must be at most {MAX_TEXT_LENGTH} characters long")

    if len(chat_name) == 0:
        raise InappropriateChatNameError("Chat name has no printable characters")

    for char in chat_name:
        if not (32 <= ord(char) <= 126 or 1040 <= ord(char) <= 1103):
            raise InappropriateChatNameError("Illegal characters in the chat name")

    return chat_name


class CreateChatRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, chat_name: str) -> str:
        chat_name = validate_chat_name(chat_name)
        return chat_name


class Chat(BaseModel):
    id: int = Field(ge=1)
    name: str


class GetChatsResponse(BaseModel):
    chats: List[Chat]


class JoinChatRequest(BaseModel):
    chat_id: int = Field(ge=1)


class GenericMessageResponse(BaseModel):
    message: str
