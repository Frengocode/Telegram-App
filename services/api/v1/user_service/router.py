from fastapi import Depends, APIRouter, File, UploadFile
from protos import user_pb2_grpc, user_pb2
from services.api.v1.user_service.scheme import (
    CreateUserSceheme,
    UpdateProfileRequestScheme,
)
from services.api.v1.user_service.client import grpc_user_client
from google.protobuf.json_format import MessageToDict
from typing import Annotated
from services.api.v1.auth_service.oauth import get_current_user, SUser


user_serivce_router = APIRouter(tags=["User Service"], prefix="/user-service/api/v1")


@user_serivce_router.post("/create-user/")
async def create_user(
    request: CreateUserSceheme,
    client: Annotated[user_pb2_grpc.UserServiceStub, Depends(grpc_user_client)],
):
    response = await client.CreateUser(
        user_pb2.CreateUserRequest(
            username=request.username,
            password=request.password,
            name=request.name,
            email=request.email,
        )
    )

    return MessageToDict(response)


@user_serivce_router.get("/get-user-by-username-password/{username}/{password}/")
async def get_user_by_useranme_password(
    username: str,
    password: str,
    client: Annotated[user_pb2_grpc.UserServiceStub, Depends(grpc_user_client)],
):
    response = await client.GetUserByUsernamePassword(
        user_pb2.GetUserByUsernamePasswordRequest(username=username, password=password)
    )

    return MessageToDict(response)


@user_serivce_router.get("/get-user/{username}/")
async def get_user(
    username: str,
    client: Annotated[user_pb2_grpc.UserServiceStub, Depends(grpc_user_client)],
):
    response = await client.GetUser(user_pb2.GetUserRequest(username=username))

    return MessageToDict(response)


@user_serivce_router.get("/get-user-by-id/{id}/")
async def get_user_by_id(
    id: int,
    client: Annotated[user_pb2_grpc.UserServiceStub, Depends(grpc_user_client)],
):
    response = await client.GetUserByID(user_pb2.GetUserByIdRequest(id=id))

    return MessageToDict(response)


@user_serivce_router.patch("/update-user-profile/")
async def update_profile(
    client: Annotated[user_pb2_grpc.UserServiceStub, Depends(grpc_user_client)],
    request: UpdateProfileRequestScheme,
    current_user: Annotated[SUser, Depends(get_current_user)],
):
    response = await client.UpdateProfile(
        user_pb2.UpdateProfileRequest(
            user_id=int(current_user.id),
            username=request.username,
            surname=request.surname,
            name=request.name,
            email=request.email,
        )
    )

    return MessageToDict(response)


@user_serivce_router.patch("/update-profile-picture/")
async def update_profile_picture(
    client: Annotated[user_pb2_grpc.UserServiceStub, Depends(grpc_user_client)],
    current_user: Annotated[SUser, Depends(get_current_user)],
    profile_picture: UploadFile = File(...),
):

    file_content = await profile_picture.read()

    response = await client.UpdateProfilePicture(
        user_pb2.UpdateProfilePictureRequest(
            profile_picture=file_content, user_id=int(current_user.id)
        )
    )

    return MessageToDict(response)
