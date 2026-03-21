from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_asyncsession
from app.chat.schemas import (
    SendTextMessageRequest,
    GetMessagesResponse,
    CreateChatRequest,
    GetChatsResponse,
    JoinChatRequest,
    GenericMessageResponse
)

from app.auth.dependencies import get_current_user_id
from app.repositories.messages import (
    insert_message
)
from app.repositories.chats import (
    insert_chat,
    select_chats
)
from app.repositories.chat_members import (
    insert_chat_member,
)
from app.chat.services import fetch_messages, add_member_to_chat

SessionDep = Annotated[AsyncSession, Depends(get_asyncsession)]
UserIdDep = Annotated[int, Depends(get_current_user_id)]

chat_router = APIRouter(prefix="/chat",
tags=["Chat"])


@chat_router.post("/send")
async def send(
    request: SendTextMessageRequest,
    sender_id: UserIdDep,
    session: SessionDep) -> GenericMessageResponse:

    chat_id, content = request.chat_id, request.content

    await insert_message(session, sender_id, chat_id, content)

    return GenericMessageResponse(message="Message sent successfully")


@chat_router.get("/messages")
async def get_messages(
    chat_id: int,
    after_id: int,
    session: SessionDep) -> GetMessagesResponse:

    messages = await fetch_messages(session, chat_id, after_id)

    return GetMessagesResponse(messages=messages)


@chat_router.get("/list")
async def get_chats_list(
    user_id: UserIdDep,
    session: SessionDep) -> GetChatsResponse:
    chats = await select_chats(session, user_id)

    return GetChatsResponse(chats=chats)


@chat_router.post("/create")
async def create_chat(
    request: CreateChatRequest,
    creator_id: UserIdDep,
    session: SessionDep) -> GenericMessageResponse:

    name = request.name

    new_chat_id = await insert_chat(session, name)
    await insert_chat_member(session, new_chat_id, creator_id)
    return GenericMessageResponse(message="Successful chat creation")


@chat_router.post("/join")
async def join_chat(
    request: JoinChatRequest,
    user_id: UserIdDep,
    session: SessionDep) -> GenericMessageResponse:

    chat_id = request.chat_id

    await add_member_to_chat(session, chat_id, user_id)
    return GenericMessageResponse(message="Successful chat join")
