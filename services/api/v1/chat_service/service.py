from grpc import aio
import asyncio
from google.protobuf.empty_pb2 import Empty
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from database.chat_database import get_chat_sesison, async_session_maker
from uitils.scheme import SUser
from protos import chat_pb2, chat_pb2_grpc
from services.api.v1.chat_service.models import ChatModel
from uitils.utils import log
from services.api.v1.auth_service.oauth import get_current_user
import httpx
import grpc
import json


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(
        self, session: AsyncSession = None, current_user: SUser = None
    ) -> object:
        self.session = session
        self.current_user = current_user

    async def CreateChat(self, request, context=None):

        log.info(f"author id {request.author_id}")

        exist_chat = (
            (
                await self.session.execute(
                    select(ChatModel).filter_by(
                        chat_member_id=request.member_id,
                        chat_author_id=request.author_id,
                    )
                )
            )
            .scalars()
            .first()
        )

        if exist_chat:
            log.info(f"Chat All ready created with this user {request.member_id}")
            return Empty()

        member_data = await self.get_data_from_url(
            f"http://localhost:8000/user-service/api/v1/get-user-by-id/{request.member_id}/"
        )
        if member_data:

            chat = ChatModel(
                chat_author_id=request.author_id,
                chat_member_id=int(member_data.get("user").get("id")),
            )

        try:
            self.session.add(chat)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            context.set_details(f"Error creating user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return chat_pb2.CreateChatResponse()

        log.info("Chat Created Succsesfully")

        return chat_pb2.CreateChatResponse(
            chat=chat_pb2.Chat(
                chat_member_id=int(member_data.get("user").get("id")),
                chat_author_id=request.author_id,
            )
        )

    async def GetUserChats(self, request, context):
        chats = (
            (
                await self.session.execute(
                    select(ChatModel)
                    .order_by(ChatModel.created_at.desc())
                    .filter(
                        or_(
                            ChatModel.chat_member_id == request.author_id,
                            ChatModel.chat_author_id == request.author_id,
                        )
                    )
                )
            )
            .scalars()
            .all()
        )

        if not chats:
            return Empty()

        user_data_map = {}
        for chat in chats:
            try:
                user_data = await self.get_data_from_url(
                    f"http://localhost:8000/user-service/api/v1/get-user-by-id/{chat.chat_member_id}/"
                )
                if user_data and "user" in user_data:  # Проверяем наличие данных
                    user_data_map[chat.chat_member_id] = user_data["user"]
            except Exception as e:
                print(f"Error fetching user data for {chat.chat_member_id}: {e}")

        author_data_map = {}
        for chat in chats:
            try:
                user_data = await self.get_data_from_url(
                    f"http://localhost:8000/user-service/api/v1/get-user-by-id/{chat.chat_author_id}/"
                )
                if user_data and "user" in user_data:
                    author_data_map[chat.chat_author_id] = user_data["user"]
            except Exception as e:
                print(f"Error fetching user data for {chat.chat_member_id}: {e}")

        chat_response = [
            chat_pb2.Chat(
                id=chat.id,
                chat_author_id=chat.chat_author_id,
                chat_member_id=chat.chat_member_id,
                chat_author=chat_pb2.ChatUser(
                    id=int(author_data_map.get(chat.chat_author_id, {}).get("id", 0)),
                    username=author_data_map.get(chat.chat_author_id, {}).get(
                        "username", ""
                    ),
                    profile_picture=author_data_map.get(chat.chat_author_id, {}).get(
                        "profile_picture", ""
                    ),
                    name=author_data_map.get(chat.chat_author_id, {}).get("name", ""),
                    surname=author_data_map.get(chat.chat_author_id, {}).get(
                        "surname", ""
                    ),
                    age=author_data_map.get(chat.chat_author_id, {}).get("age", 0),
                    email=author_data_map.get(chat.chat_author_id, {}).get("email", ""),
                ),
                chat_member=chat_pb2.ChatUser(
                    id=int(user_data_map.get(chat.chat_member_id, {}).get("id", 0)),
                    username=user_data_map.get(chat.chat_member_id, {}).get(
                        "username", ""
                    ),
                    profile_picture=user_data_map.get(chat.chat_member_id, {}).get(
                        "profile_picture", ""
                    ),
                    name=user_data_map.get(chat.chat_member_id, {}).get("name", ""),
                    surname=user_data_map.get(chat.chat_member_id, {}).get(
                        "surname", ""
                    ),
                    age=user_data_map.get(chat.chat_member_id, {}).get("age", 0),
                    email=user_data_map.get(chat.chat_member_id, {}).get("email", ""),
                ),
            )
            for chat in chats
        ]

        return chat_pb2.GetUserChatsResponse(
            chat=chat_response,
        )

    async def GetUserChat(self, request, context):

        chat = (
            (
                await self.session.execute(
                    select(ChatModel)
                    .filter(ChatModel.id == request.id)
                    .filter(
                        or_(
                            ChatModel.chat_author_id == request.author_id,
                            ChatModel.chat_member_id == request.author_id,
                        )
                    )
                )
            )
            .scalars()
            .first()
        )

        if not chat:
            log.info("Chat Not Found")
            return Empty()

        chat_members_data = await self.get_data_from_url(
            f"http://localhost:8000/user-service/api/v1/get-user-by-id/{chat.chat_member_id}/"
        )

        log.info(f"Getting User Chat {request.id}")
        return chat_pb2.GetUserChatResponse(
            chat=chat_pb2.Chat(
                id = chat.id,
                chat_author_id=int(chat.chat_author_id),
                chat_member_id=chat.chat_member_id,
                chat_member=chat_pb2.ChatUser(
                    id=int(chat_members_data.get("user").get("id")),
                    username=chat_members_data.get("user").get("username"),
                    profile_picture=chat_members_data.get("profile_picture"),
                ),
            ),
        )

    async def DeleteChat(self, request, context):
        chat = (
            (
                await self.session.execute(
                    select(ChatModel)
                    .filter_by(id=request.id)
                    .filter(
                        or_(
                            ChatModel.chat_author_id == request.author_id,
                            ChatModel.chat_member_id == request.author_id,
                        )
                    )
                )
            )
            .scalars()
            .first()
        )

        if not chat:
            log.info("Chat Not Found Or User Error")
            return Empty()

        log.info("Deleted Succsesfully")
        await self.session.delete(chat)
        await self.session.commit()

        return chat_pb2.DeleteChatResponse(message="Deleted Succsesfully")

    async def get_data_from_url(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}")
            if response is not None:
                return response.json()
            return None


async def chat_run(addr="localhost:50053"):
    server = aio.server()

    async with async_session_maker() as session:
        chat_service = ChatService(session=session)

    # # async with get_current_user() as cr:
    # chat_service = ChatService()

    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_service, server)
    server.add_insecure_port(addr)

    log.warning(f"Starting server on {addr}")
    await server.start()
    await server.wait_for_termination()
    log.error(f"Error while starting the server:")


if __name__ == "__main__":
    asyncio.run(chat_run())
