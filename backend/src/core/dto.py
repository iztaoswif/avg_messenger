from dataclasses import dataclass
from datetime import datetime

from core.helper_types import ChatId, MessageId, UserId


@dataclass
class Message:
    id: MessageId
    sender_id: UserId
    content: str
    created_at: datetime


@dataclass
class Chat:
    id: ChatId
    name: str


@dataclass
class User:
    id: UserId
    username: str
