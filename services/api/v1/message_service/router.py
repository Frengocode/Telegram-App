from fastapi import APIRouter, Depends
from uitils.scheme import SUser
from services.api.v1.auth_service.oauth import get_current_user
from protos import message_pb2, message_pb2_grpc
from typing import Optional, Annotated
from services.api.v1.message_service.sheme import CreateMessageRequestScheme
from services.api.v1.message_service.client import grpc_message_client
from google.protobuf.json_format import MessageToDict



message_service_router = APIRouter(tags=["Message Service"], prefix="/message-service/api/v1")



@message_service_router.post("/create-message/")
async def create_message(client: Annotated[message_pb2_grpc.MessageServiceStub, Depends(grpc_message_client)], current_user: Annotated[SUser, Depends(get_current_user)], request: CreateMessageRequestScheme):
    response = await client.CreateMessage(
        message_pb2.CreateMessageRequest(
            chat_id=request.chat_id,
            message=request.message,
            user_id=int(current_user.id),
            token=current_user.token
        )
    )

    return MessageToDict(response)