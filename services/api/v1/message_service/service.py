from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from sqlalchemy.ext.asyncio import AsyncSession
from google.protobuf.json_format import MessageToDict, MessageToJson
from google.protobuf.empty_pb2 import Empty
from sqlalchemy import select
from protos import message_pb2, message_pb2_grpc
from database.message_database import get_message_sesison, async_session_maker
from services.api.v1.message_service.models import MessageModel
from redis.asyncio import StrictRedis
from uitils.utils import log, get_redis_client
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
    def __init__(self, session: AsyncSession, redis_cli: StrictRedis = None):
        self.session = session
        self.redis_cli = redis_cli

    async def CreateMessage(self, request, context):

        chat = await self._get_data_from_url(
            f"http://localhost:8000/chat-service/api/v1/get-user-chat/{request.chat_id}/",
            access_token=request.token,
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
            return message_pb2.GetMessagesResponse(message=[])

        user_data_map = {}
        for message in messages:
            try:
                user_data = await self._get_data_from_url(
                    f"http://localhost:8000/user-service/api/v1/get-user-by-id/{message.user_id}/",
                    access_token=request.token,
                    cache_name=f"get-user-by-id-{str(message.user_id)}",
                )

                if isinstance(user_data, str):
                    user_data = json.loads(user_data)

                user = user_data.get("user", {})
                user_data_map[message.user_id] = user

            except Exception as e:
                log.error(f"Error fetching user data for {message.user_id}: {e}")

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
                        "profilePicture", ""
                    ),
                    name=user_data_map.get(message.user_id, {}).get("name", ""),
                    surname=user_data_map.get(message.user_id, {}).get("surname", ""),
                ),
            )
            for message in messages
        ]

        if not message_response:
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

    async def _get_data_from_url(
        self, url: str, access_token: str = None, cache_name: str = None
    ):
        cached_data = await self.get_data_from_cache(cache_name)
        if cached_data:
            return json.dumps(cached_data)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
            )

        if response.status_code == 200:
            data = response.json()
            if cache_name:
                await self.redis_cli.setex(cache_name, 300, json.dumps(data))
            return data

        return None

    async def get_data_from_cache(self, cache_name: str):
        if not cache_name:
            return None

        cached_data = await self.redis_cli.get(cache_name)
        if cached_data:
            return json.loads(cached_data)

        return None


async def message_run(addr="localhost:50054"):
    server = grpc.aio.server()

    async with async_session_maker() as session:
        redis_cli = await get_redis_client()
        message_service = MessgaeService(session=session, redis_cli=redis_cli)

    message_pb2_grpc.add_MessageServiceServicer_to_server(message_service, server)
    server.add_insecure_port(addr)

    log.warning(f"Starting server on {addr}")
    await server.start()
    await server.wait_for_termination()
    log.error(f"Error while starting the server:")


if __name__ == "__main__":
    asyncio.run(message_run())
