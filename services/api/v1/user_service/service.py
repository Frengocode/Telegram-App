from fastapi import HTTPException, File, UploadFile
from services.api.v1.user_service.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from protos import user_pb2, user_pb2_grpc
from uitils.utils import Hash, get_redis_client
from sqlalchemy import select
from google.protobuf.json_format import MessageToDict, MessageToJson
from database.user_database import async_session_maker
from uitils.utils import log
from google.protobuf.empty_pb2 import Empty
from redis.asyncio import StrictRedis
from datetime import datetime
from grpc import aio
import grpc
import asyncio
import json
import aiofiles
import os
import uuid

MEDIA_ROOT = "media/profile_picture/"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, session: AsyncSession, redis_cli: StrictRedis) -> None:
        self.session = session
        self.redis_cli = redis_cli

    async def CreateUser(self, request, context):
        # Check if user already exists
        exist_user = (
            (
                await self.session.execute(
                    select(UserModel).filter_by(
                        username=request.username, email=request.email
                    )
                )
            )
            .scalars()
            .first()
        )

        if exist_user:
            context.set_details("User already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return user_pb2.CreateUserResponse()

        ###### HASHING PASSWORD #######
        hashed_password = Hash.bcrypt(request.password)

        ##### CREATING USER
        user = UserModel(
            username=request.username,
            email=request.email,
            password=hashed_password,
            name=request.name,
        )

        try:
            self.session.add(user)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            context.set_details(f"Error creating user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_pb2.CreateUserResponse()

        return user_pb2.CreateUserResponse(
            user=user_pb2.User(username=request.username, name=request.name)
        )

    async def GetUserByUsernamePassword(self, request, context):
        user = (
            (
                await self.session.execute(
                    select(UserModel).filter_by(username=request.username)
                )
            )
            .scalars()
            .first()
        )

        if not user:
            log.info("User Not Found")
            return HTTPException(detail="User Not Found", status_code=404)

        if not Hash.verify(request.password, user.password):
            context.set_details(f"Password Error")
            return user_pb2.GetUserByUsernamePasswordResponse()

        log.info(f"Getting User Data <ID :{user.id}: USERNAME :{user.username}: ")

        return user_pb2.GetUserByUsernamePasswordResponse(
            user=user_pb2.User(
                id=user.id,
                username=user.username,
                surname=user.surname,
                name=user.name,
                profile_picture=user.picture_url,
                email=user.email,
                age=user.age,
            )
        )

    async def GetUser(self, request, context):
        cached_data = await self.get_data_from_cache(
            f"get-user-by-username-{request.username}"
        )
        if cached_data:
            return user_pb2.GetUserResponse(
                id=int(cached_data.get("id")),
                username=cached_data.get("username"),
                email=cached_data.get("email"),
                surname=cached_data.get("surname"),
                name=cached_data.get("name"),
            )

        user = (
            (
                await self.session.execute(
                    select(UserModel).filter_by(username=request.username)
                )
            )
            .scalars()
            .first()
        )

        if not user:
            log.info(f"User not found with username {request.username}")
            return Empty()

        user_response = user_pb2.GetUserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            profile_picture=user.picture_url,
            name=user.name,
            surname=user.surname,
        )

        user_response_json = MessageToJson(user_response)

        await self.redis_cli.setex(
            f"get-user-by-username-{request.username}", 100, user_response_json
        )

        return user_response

    async def GetUserByID(self, request, context):

        cached_data = await self.get_data_from_cache(f"get-user-by-id-{request.id}")
        if cached_data:
            return user_pb2.GetUserByIdResponse(
                user=user_pb2.User(
                    id=int(cached_data.get("user").get("id")),
                    username=cached_data.get("user").get("username"),
                    surname=cached_data.get("user").get("surname"),
                    email=cached_data.get("user").get("email"),
                    name=cached_data.get("user").get("name"),
                    age=cached_data.get("user").get("age"),
                )
            )

        user = (
            (await self.session.execute(select(UserModel).filter_by(id=request.id)))
            .scalars()
            .first()
        )

        if not user:
            log.info(f"User not Found with id {request.id}")
            return Empty()

        user_response = user_pb2.GetUserByIdResponse(
            user=user_pb2.User(
                id=user.id,
                username=user.username,
                profile_picture=user.picture_url,
                age=user.age,
                email=user.email,
                name=user.name,
                surname=user.surname,
            )
        )

        user_response_dict = MessageToJson(user_response)

        await self.redis_cli.setex(
            f"get-user-by-id-{request.id}", 100, user_response_dict
        )

        log.info(f"Getting Data for user id {request.id}")
        return user_pb2.GetUserByIdResponse(
            user=user_pb2.User(
                id=user.id,
                username=user.username,
                profile_picture=user.picture_url,
                age=user.age,
                email=user.email,
                name=user.name,
                surname=user.surname,
            )
        )

    async def UpdateProfile(self, request, context):

        user = (
            (
                await self.session.execute(
                    select(UserModel).filter_by(id=request.user_id)
                )
            )
            .scalars()
            .first()
        )

        if not user:
            log.info(f"User Error, {request.id} This User cant update profile !")
            return Empty()

        exist_username = (
            (
                await self.session.execute(
                    select(UserModel).filter_by(username=request.username)
                )
            )
            .scalars()
            .first()
        )

        if exist_username:
            log.info("This Username All ready Used")
            return Empty()

        for name, value in request.DESCRIPTOR.fields_by_name.items():
            if hasattr(user, name) and value:
                setattr(user, name, getattr(request, name))

        log.info("Profile updated succsesfully")
        await self.redis_cli.delete(f"get-user-by-username-{user.username}")
        await self.session.commit()

        return Empty()

    async def get_data_from_cache(self, cahche_name: str):
        cached_data = await self.redis_cli.get(cahche_name)
        log.info(f"Getting data from cache {cahche_name}")
        if cached_data:
            return json.loads(cached_data)
        return None

    async def UpdateProfilePicture(self, request, context):

        user = (
            (
                await self.session.execute(
                    select(UserModel).filter_by(id=request.user_id)
                )
            )
            .scalars()
            .first()
        )

        if not user:
            log.info("User Not Found")
            return Empty()
        if user.picture_url is not None:
            exist_user_profile_picture = os.path.join(MEDIA_ROOT, user.picture_url)
            if exist_user_profile_picture:
                os.remove(exist_user_profile_picture)

        if request.profile_picture:
            file_name = f"{uuid.uuid4()}.jpg"
            file_path = os.path.join(MEDIA_ROOT, file_name)

            async with aiofiles.open(file_path, "wb") as out_file:
                await out_file.write(request.profile_picture)

            log.info(f"Picture {file_name} saved at {file_path}")

            user.picture_url = file_name

            await self.session.commit()

            return user_pb2.UpdateProfilePictureResponse(profile_picture=file_name)

        log.info("No profile picture provided")
        return Empty()


async def run(addr="localhost:50051"):
    server = aio.server()

    async with async_session_maker() as session:
        redis_cli = await get_redis_client()
        user_service = UserService(session=session, redis_cli=redis_cli)

        user_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)
        server.add_insecure_port(addr)

        log.warning(f"Starting server on {addr}")
        await server.start()
        await server.wait_for_termination()
        log.error(f"Error while starting the server:")


if __name__ == "__main__":
    asyncio.run(run())
