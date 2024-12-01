from sqlalchemy.ext.asyncio import AsyncSession
from google.protobuf.empty_pb2 import Empty
from sqlalchemy import select
from protos import message_pb2, message_pb2_grpc
from database.message_database import get_message_sesison, async_session_maker
from services.api.v1.message_service.models import MessageModel
from uitils.utils import log
import httpx
import grpc
import asyncio


class MessgaeService(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def CreateMessage(self, request, context):
        
        chat = await self._get_data_from_url(f"http://localhost:8000/chat-service/api/v1/get-user-chat/{request.chat_id}/", accses_token=request.token)
        if chat is None:
            log.info("Chat Not Found")
            return Empty()
        
        message = MessageModel(
            message = request.message,
            chat_id = request.chat_id,
            user_id = request.user_id
        )

        self.session.add(message)
        await self.session.commit()

        return message_pb2.CreateMessageResponse(
            message=message_pb2.Message(
                message=request.message,
                user_id=request.user_id,
                chat_id=request.chat_id
                
            )
        )
    
    async def _get_data_from_url(self, url: str, accses_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {accses_token}"},)
            if response is not None:
                return response.json()
            return None
        




async def message_run(addr="localhost:50054"):
    server = grpc.aio.server()

    async with async_session_maker() as session:
        message_service = MessgaeService(session=session)

    # # async with get_current_user() as cr:
    # chat_service = ChatService()

    message_pb2_grpc.add_MessageServiceServicer_to_server(message_service, server)
    server.add_insecure_port(addr)

    log.warning(f"Starting server on {addr}")
    await server.start()
    await server.wait_for_termination()
    log.error(f"Error while starting the server:")


if __name__ == "__main__":
    asyncio.run(message_run())
