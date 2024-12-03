from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from sqlalchemy.ext.asyncio import AsyncSession
from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty
from sqlalchemy import select
from protos import message_pb2, message_pb2_grpc
from database.message_database import get_message_sesison, async_session_maker
from services.api.v1.message_service.models import MessageModel
from uitils.utils import log
from datetime import datetime
import httpx
import grpc
import asyncio
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: int):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id: int, message: dict):
        if chat_id in self.active_connections:
            if "timestamp" in message and isinstance(message["timestamp"], datetime):
                message["timestamp"] = message["timestamp"].isoformat()

            for connection in self.active_connections[chat_id]:
                await connection.send_json(message)


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket, chat_id)

    try:
        while True:
            data = await websocket.receive_text()

            message_data = json.loads(data)

            if "timestamp" in message_data and isinstance(
                message_data["timestamp"], datetime
            ):
                message_data["timestamp"] = message_data["timestamp"].isoformat()

            message_data["user"] = message_data.get("user", "Unknown")
            message_data["profile_photo"] = message_data.get(
                "user.profile_picture", None
            )

            await manager.broadcast(chat_id, message_data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)


class MessgaeService(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def CreateMessage(self, request, context):

        chat = await self._get_data_from_url(
            f"http://localhost:8000/chat-service/api/v1/get-user-chat/{request.chat_id}/",
            accses_token=request.token,
        )
        if chat is None:
            log.info("Chat Not Found")
            return Empty()

        message = MessageModel(
            message=request.message, chat_id=request.chat_id, user_id=request.user_id
        )

        self.session.add(message)
        await self.session.commit()

        return message_pb2.Message(
            message=request.message,
            user_id=request.user_id,
            chat_id=request.chat_id,
            user=message_pb2.MessageUser(
                id=request.user_id,
                username=request.username,
                profile_picture=request.profile_picture,
                name=request.name,
            ),
        )

    async def GetMessages(self, request, context):
        messages = (
            (
                await self.session.execute(
                    select(MessageModel).filter_by(chat_id=request.chat_id)
                )
            )
            .scalars()
            .all()
        )

        if not messages:
            return message_pb2.GetMessagesResponse(messages=[])

        user_data_map = {}
        for message in messages:
            try:
                user_data = await self._get_data_from_url(
                    f"http://localhost:8000/user-service/api/v1/get-user-by-id/{message.user_id}/",
                    accses_token=request.token,
                )
                if user_data and "user" in user_data:
                    user_data_map[message.user_id] = user_data["user"]
            except Exception as e:
                log.info(f"Error fetching user data for {message.user_id}: {e}")

        message_response = [
            message_pb2.Message(
                id=message.id,
                message=message.message,
                chat_id=message.chat_id,
                user_id=message.user_id,
                user=message_pb2.MessageUser(
                    id=int(user_data_map.get(message.user_id, {}).get("id", 0)),
                    username=user_data_map.get(message.user_id, {}).get("username", ""),
                    profile_picture=user_data_map.get(message.user_id, {}).get(
                        "profile_picture", ""
                    ),
                    name=user_data_map.get(message.user_id, {}).get("name", ""),
                    surname=user_data_map.get(message.user_id, {}).get("surname", ""),
                ),
            )
            for message in messages
        ]

        if message_response is None:
            log.info("Messages Not Found")
            return Empty()

        return message_pb2.GetMessagesResponse(message=message_response)

    async def DeleteMessage(self, request, context):
        message = (
            (
                await self.session.execute(
                    select(MessageModel).filter_by(
                        id=request.id, user_id=request.user_id
                    )
                )
            )
            .scalars()
            .first()
        )

        if not message:
            log.info("Message Not Found")
            return Empty()

        log.info("Deleted Succsesfully")
        await self.session.delete(message)
        await self.session.commit()

        return Empty()

    async def UpdateMessage(self, request, context):
        message = (
            (await self.session.execute(select(MessageModel).filter_by(id=request.id)))
            .scalars()
            .first()
        )

        if not message:
            log.info("Message Not Found")
            return Empty()

        for name, value in request.DESCRIPTOR.fields_by_name.items():
            if hasattr(message, name) and value:
                setattr(message, name, getattr(request, name))

        log.info(f"Message Updated Succsesuflly, id {message.id}")

        await self.session.commit()

        return Empty()

    async def _get_data_from_url(self, url: str, accses_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {accses_token}"},
            )
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
