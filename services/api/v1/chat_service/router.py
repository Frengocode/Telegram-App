from fastapi import APIRouter, Depends
from services.api.v1.chat_service.service import ChatService, get_chat_sesison
from services.api.v1.auth_service.oauth import get_current_user
from protos import chat_pb2, chat_pb2_grpc
from services.api.v1.chat_service.client import grpc_chat_client
from uitils.scheme import SUser
from typing import Annotated
from services.api.v1.chat_service.scheme import CreateChatRequest
from google.protobuf.json_format import MessageToDict
from sqlalchemy.ext.asyncio import AsyncSession
from uitils.utils import log
import json


chat_service_router = APIRouter(tags=["Chat Service"], prefix="/chat-service/api/v1")


@chat_service_router.post("/create-chat/")
async def create_chat(
    request: CreateChatRequest,
    current_user: Annotated[SUser, Depends(get_current_user)],
    client: Annotated[chat_pb2_grpc.ChatServiceStub, Depends(grpc_chat_client)],
):

    log.info(f"{current_user}")
    response = await client.CreateChat(
        chat_pb2.CreateChatRequest(
            member_id=request.member_id, author_id=int(current_user.id)
        ),
    )
    return MessageToDict(response)


@chat_service_router.get("/get-user-chats/")
async def get_user_chats(
    client: Annotated[chat_pb2_grpc.ChatServiceStub, Depends(grpc_chat_client)],
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    response = await client.GetUserChats(
        chat_pb2.GetUserChatsRequest(
            author_id=int(current_user.id),
        )
    )

    return MessageToDict(response)


@chat_service_router.get("/get-user-chat/{id}/")
async def get_user_chat(
    id: int,
    client: chat_pb2_grpc.ChatServiceStub = Depends(grpc_chat_client),
    current_user: SUser = Depends(get_current_user),
):
    response = await client.GetUserChat(
        chat_pb2.GetUserChatRequest(author_id=int(current_user.id), id=id)
    )

    return MessageToDict(response)


@chat_service_router.delete("/delete-user-chat/{id}/")
async def delete_chat(
    id: int,
    client: Annotated[chat_pb2_grpc.ChatService, Depends(grpc_chat_client)],
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    response = await client.DeleteChat(
        chat_pb2.DeleteChatRequest(id=id, author_id=int(current_user.id))
    )

    return MessageToDict(response)
