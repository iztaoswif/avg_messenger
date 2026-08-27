from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencies import get_asyncsession
from chat.schemas import (
    SendTextMessageRequest,
    GetMessagesResponse,
    CreateChatRequest,
    CreateChatResponse,
    GetChatsResponse,
    GetChatResponse,
    JoinChatRequest,
    AddUserRequest,
    GenericMessageResponse
)
from auth.dependencies import get_current_user_id
from repositories.chats import (
    select_chats_of_user
)
from chat.services import (
    ensure_chat_access,
    ensure_user_exists,
    fetch_messages,
    add_member_to_chat,
    create_message_in_chat,
    add_new_chat,
    fetch_chat_name_by_id
)
from chat.exceptions import SelfReferencingError

SessionDep = Annotated[AsyncSession, Depends(get_asyncsession)]
UserIdDep = Annotated[int, Depends(get_current_user_id)]

chat_router = APIRouter(prefix="/chat",
tags=["Chat"])


@chat_router.post("/send")
async def send_message(
    request: SendTextMessageRequest,
    sender_id: UserIdDep,
    session: SessionDep,
) -> GenericMessageResponse:
    await ensure_chat_access(session, request.chat_id, sender_id)

    await create_message_in_chat(
        session,
        sender_id,
        request.chat_id,
        request.content
    )

    return GenericMessageResponse(message="Message sent successfully")


@chat_router.get("/messages")
async def get_messages(
    chat_id: int,
    after_id: int,
    user_id: UserIdDep,
    session: SessionDep
) -> GetMessagesResponse:
    await ensure_chat_access(session, chat_id, user_id)
    messages = await fetch_messages(session, chat_id, after_id)

    return GetMessagesResponse(messages=messages)


@chat_router.get("/list")
async def get_chats_list(
    user_id: UserIdDep,
    session: SessionDep
) -> GetChatsResponse:
    chats = await select_chats_of_user(session, user_id)

    return GetChatsResponse(chats=chats)


@chat_router.get("/{chat_id}")
async def get_chat_name(
    chat_id: int,
    session: SessionDep
) -> GetChatResponse:
    chat_name = await fetch_chat_name_by_id(session, chat_id)

    return GetChatResponse(chat_name=chat_name)


@chat_router.post("/create")
async def create_chat(
    request: CreateChatRequest,
    creator_id: UserIdDep,
    session: SessionDep
) -> CreateChatResponse:
    new_chat_id = await add_new_chat(session, request.name, creator_id)

    return CreateChatResponse(
        id=new_chat_id,
        name=name
    )


@chat_router.post("/add")
async def add_new_user(
    request: AddUserRequest,
    adding_user_id: UserIdDep,
    session: SessionDep
) -> GenericMessageResponse:

    new_user_id, chat_id = request.new_user_id, request.chat_id

    if new_user_id == adding_user_id:
        raise SelfReferencingError()

    await add_member_to_chat(session, chat_id, new_user_id)


    return GenericMessageResponse(message="Successfully added new user")


'''
@chat_router.post("/join")
async def join_chat(
    request: JoinChatRequest,
    user_id: UserIdDep,
    session: SessionDep) -> GenericMessageResponse:

    chat_id = request.chat_id

    await add_member_to_chat(session, chat_id, user_id)

    await session.commit()

    return GenericMessageResponse(message="Successful chat join")
'''