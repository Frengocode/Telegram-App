from sqlalchemy.ext.asyncio import AsyncSession
from protos import history_pb2, history_pb2_grpc
from uitils.scheme import SUser
from uitils.utils import log, get_redis_client
from services.api.v1.history_service.models import HistoryModel
from database.history_database import session
from grpc import aio
import httpx
import os
import aiofiles
import uuid
from redis.asyncio import StrictRedis
from sqlalchemy import select
from google.protobuf.empty_pb2 import Empty
import json
from google.protobuf.json_format import MessageToJson


MEDIA_ROOT = "media/historys/"


class HistoryService(history_pb2_grpc.HistoryServiceServicer):
    def __init__(self, session: AsyncSession, redis_cli: StrictRedis):
        self.session = session
        self.r_cli = redis_cli

    async def CreateHistory(self, request, context):

        if request.content:
            file_name = f"{uuid.uuid4()}.jpg"
            file_path = os.path.join(MEDIA_ROOT, file_name)

            async with aiofiles.open(file_path, "wb") as out_file:
                await out_file.write(request.content)

            log.info(f"Picture {file_name} saved at {file_path}")

        history = HistoryModel(
            content_title=request.content_title,
            user_id=request.user_id,
            content=file_name,
        )

        self.session.add(history)
        await self.session.commit()

        return history_pb2.CreateHistoryResponse(
            history=history_pb2.History(
                content=file_name,
                content_title=request.content_title,
                user_id=request.user_id,
            )
        )

    async def GetHystorys(self, request, context):
        histoties = (
            (
                await self.session.execute(
                    select(HistoryModel).filter_by(user_id=request.user_id)
                )
            )
            .scalars()
            .all()
        )

        if not histoties:
            return history_pb2.GetHistorysResponse(historys=[])

        user_data_map = {}
        for history in histoties:
            try:
                user_data = await self.get_data_from_url(
                    f"http://localhost:8000/user-service/api/v1/get-user-by-id/{history.user_id}/",
                    cache_name=f"get-user-by-id-{str(history.user_id)}",
                )

                if isinstance(user_data, str):
                    user_data = json.loads(user_data)

                user = user_data.get("user", {})
                user_data_map[history.user_id] = user

            except Exception as e:
                log.error(f"Error fetching user data for {history.user_id}: {e}")

        history_response = [
            history_pb2.History(
                id=history.id,
                content=history.content,
                content_title=history.content_title,
                user_id=history.user_id,
                user=history_pb2.HistoryUser(
                    id=int(user_data_map.get(history.user_id, {}).get("id", 0)),
                    username=user_data_map.get(history.user_id, {}).get("username", ""),
                    profile_picture=user_data_map.get(history.user_id, {}).get(
                        "profilePicture", ""
                    ),
                    name=user_data_map.get(history.user_id, {}).get("name", ""),
                    surname=user_data_map.get(history.user_id, {}).get("surname", ""),
                ),
            )
            for history in histoties
        ]

        if not history_response:
            log.info("Messages Not Found")
            return Empty()

        return history_pb2.GetHistorysResponse(historys=history_response)

    async def GetHistory(self, request, context):
        history = (
            (await self.session.execute(select(HistoryModel).filter_by(id=request.id)))
            .scalars()
            .first()
        )

        if not history:
            log.info("History not found %s", request.id)
            return Empty()

        cached_data = await self.get_data_from_cache(f"get-history-{request.id}")

        if isinstance(cached_data, str):
            cached_data = json.loads(cached_data)
            cached_user_data = cached_data.get("history").get("user")

        if cached_data:

            return history_pb2.GetHistoryResponse(
                history=history_pb2.History(
                    id=int(cached_data.get("history").get("id")),
                    content=cached_data.get("history").get("content"),
                    content_title=cached_data.get("history").get("contentTitle"),
                    user=history_pb2.HistoryUser(
                        id=int(cached_user_data.get("id")),
                        username=cached_user_data.get("username"),
                        profile_picture=cached_user_data.get("profilePicture"),
                        name=cached_user_data.get("name"),
                    ),
                )
            )

        user_data = await self.get_data_from_url(
            f"http://localhost:8000/user-service/api/v1/get-user-by-id/{history.user_id}/",
            cache_name=f"get-user-by-id-{str(history.user_id)}",
        )

        if isinstance(user_data, str):
            user_data = json.loads(user_data)

        user = user_data.get("user", {})

        response = history_pb2.GetHistoryResponse(
            history=history_pb2.History(
                id=history.id,
                content=history.content,
                content_title=history.content_title,
                user=history_pb2.HistoryUser(
                    id=int(user.get("id")),
                    username=user.get("username"),
                    name=user.get("name"),
                    profile_picture=user.get("profilePicture"),
                ),
            )
        )

        history_json = MessageToJson(response)

        await self.r_cli.setex(
            f"get-history-{request.id}", 300, json.dumps(history_json)
        )

        return response

    async def DeleteHistory(self, request, context):
        history = (
            (
                await self.session.execute(
                    select(HistoryModel).filter_by(
                        id=request.id, user_id=request.user_id
                    )
                )
            )
            .scalars()
            .first()
        )

        if not history:
            log.info("history not found %s", request.id)
            return Empty()

        await self.session.delete(history)
        await self.session.commit()

        return history_pb2.DeleteHistoryResponse(response="Deleted Succsesfully")

    async def get_data_from_url(self, url: str, cache_name: str = None):
        cached_data = await self.get_data_from_cache(cache_name)
        if cached_data:
            return json.dumps(cached_data)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
            )

        if response.status_code == 200:
            data = response.json()
            if cache_name:
                await self.r_cli.setex(cache_name, 300, json.dumps(data))
            return data

        return None

    async def get_data_from_cache(self, cache_name: str):
        if not cache_name:
            return None

        cached_data = await self.r_cli.get(cache_name)
        if cached_data:
            return json.loads(cached_data)

        return None


async def history_run(addr="localhost:50055"):
    server = aio.server()

    async with session() as se:
        redis_cli = await get_redis_client()
        history_service = HistoryService(session=se, redis_cli=redis_cli)

    history_pb2_grpc.add_HistoryServiceServicer_to_server(history_service, server)
    server.add_insecure_port(addr)

    log.warning(f"Starting server on {addr}")
    await server.start()
    await server.wait_for_termination()
    log.error(f"Error while starting the server:")
