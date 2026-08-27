from pydantic import BaseModel, field_validator, Field
from core.config import (
    MAX_TEXT_LENGTH,
    MAX_CHAT_NAME_LENGTH
)
from chat.exceptions import (
    InappropriateMessageTextError,
    InappropriateChatNameError
)
from core.helper_types import ChatId, MessageId, UserId


def validate_message_text(text: str) -> str:
    if len(text) == 0:
        raise InappropriateMessageTextError("Text must be at least 1 character long")

    text = text.strip()

    if len(text) > MAX_TEXT_LENGTH:
        raise InappropriateMessageTextError(f"Text must be at most {MAX_TEXT_LENGTH} characters long")

    if len(text) == 0:
        raise InappropriateMessageTextError("Text is empty")

    sanitized_text = "".join([char for char in text if char.isascii() and not char.isspace()])

    if len(sanitized_text) == 0:
        raise InappropriateMessageTextError("Text has no valid characters")

    return sanitized_text


class SendTextMessageRequest(BaseModel):
    chat_id: ChatId
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, content: str) -> str:
        content = validate_message_text(content)
        return content


class GetMessageResponse(BaseModel):
    message_id: MessageId
    name: str


class GetMessagesResponse(BaseModel):
    messages: list[GetMessageResponse]


def validate_chat_name(chat_name: str) -> str:
    if len(chat_name) == 0:
        raise InappropriateChatNameError("Text must be at least 1 character long")

    chat_name = chat_name.strip()

    if len(chat_name) > MAX_CHAT_NAME_LENGTH:
        raise InappropriateChatNameError(f"Chat name must be at most {MAX_TEXT_LENGTH} characters long")

    if len(chat_name) == 0:
        raise InappropriateChatNameError("Chat name has no printable characters")

    for char in chat_name:
        if not char.isascii() or char.isspace():
            raise InappropriateChatNameError("Illegal characters in the chat name")

    return chat_name


class CreateChatRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, chat_name: str) -> str:
        chat_name = validate_chat_name(chat_name)
        return chat_name


class CreateChatResponse(BaseModel):
    chat_id: ChatId
    name: str


class GetChatResponse(BaseModel):
    chat_name: str


class GetChatsResponse(BaseModel):
    chats: list[GetChatResponse]


class JoinChatRequest(BaseModel):
    chat_id: ChatId


class GenericMessageResponse(BaseModel):
    message: str


class AddUserRequest(BaseModel):
    new_user_id: UserId
    chat_id: ChatId
