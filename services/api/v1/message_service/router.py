from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from uitils.scheme import SUser
from services.api.v1.auth_service.oauth import get_current_user
from protos import message_pb2, message_pb2_grpc
from typing import Optional, Annotated
from services.api.v1.message_service.sheme import (
    CreateMessageRequestScheme,
    UpdateMessageRequestScheme,
)
from services.api.v1.message_service.client import grpc_message_client
from google.protobuf.json_format import MessageToDict, MessageToJson
from services.api.v1.message_service.service import websocket_endpoint, manager


message_service_router = APIRouter(
    tags=["Message Service"], prefix="/message-service/api/v1"
)


@message_service_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming message
            await websocket.send_text(f"Message from {user_id}: {data}")
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")


@message_service_router.post("/create-message/")
async def create_message(
    client: Annotated[
        message_pb2_grpc.MessageServiceStub, Depends(grpc_message_client)
    ],
    current_user: Annotated[SUser, Depends(get_current_user)],
    request: CreateMessageRequestScheme,
):
    response = await client.CreateMessage(
        message_pb2.CreateMessageRequest(
            chat_id=request.chat_id,
            message=request.message,
            user_id=int(current_user.id),
            token=current_user.token,
            username=current_user.username,
            name=current_user.name,
            profile_picture=current_user.profile_picture,
        )
    )

    return MessageToDict(response)


@message_service_router.get("/get-messages/{chat_id}/")
async def get_messages(
    chat_id: int,
    client: Annotated[
        message_pb2_grpc.MessageServiceStub, Depends(grpc_message_client)
    ],
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    response = await client.GetMessages(
        message_pb2.GetMessagesRequest(
            chat_id=chat_id, user_id=int(current_user.id), token=current_user.token
        )
    )

    return MessageToDict(response)


@message_service_router.delete("/delete-message/{id}/")
async def delete_message(
    client: Annotated[
        message_pb2_grpc.MessageServiceStub, Depends(grpc_message_client)
    ],
    current_user: Annotated[SUser, Depends(get_current_user)],
    id: int,
):
    response = await client.DeleteMessage(
        message_pb2.DeleteMessageRequest(id=id, user_id=int(current_user.id))
    )

    return MessageToDict(response)


@message_service_router.patch("/update-message/")
async def update_message(
    client: Annotated[
        message_pb2_grpc.MessageServiceStub, Depends(grpc_message_client)
    ],
    current_user: Annotated[SUser, Depends(get_current_user)],
    request: UpdateMessageRequestScheme,
):
    response = await client.UpdateMessage(
        message_pb2.UpdateMessageRequest(
            id=request.id, user_id=int(current_user.id), message=request.message
        )
    )

    return MessageToDict(response)
