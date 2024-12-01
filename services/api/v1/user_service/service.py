from fastapi import HTTPException
from services.api.v1.user_service.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from protos import user_pb2, user_pb2_grpc
from uitils.utils import Hash
from sqlalchemy import select
from database.user_database import async_session_maker
from uitils.utils import log
from google.protobuf.empty_pb2 import Empty
from grpc import aio
import grpc
import asyncio


class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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

        return user_pb2.GetUserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            profile_picture=user.picture_url,
            name=user.name,
            surname=user.surname,
            )

    async def GetUserByID(self, request, context):
        user = (
            (await self.session.execute(select(UserModel).filter_by(id=request.id)))
            .scalars()
            .first()
        )

        if not user:
            log.info(f"User not Found with id {request.id}")
            return Empty()

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
    



async def run(addr="localhost:50051"):
    server = aio.server()

    async with async_session_maker() as session:
        user_service = UserService(session=session)

        user_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)
        server.add_insecure_port(addr)

        log.warning(f"Starting server on {addr}")
        await server.start()
        await server.wait_for_termination()
        log.error(f"Error while starting the server:")


if __name__ == "__main__":
    asyncio.run(run())
