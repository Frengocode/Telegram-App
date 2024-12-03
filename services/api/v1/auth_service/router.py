from fastapi import APIRouter, Depends, HTTPException, security
from protos import auth_pb2, auth_pb2_grpc
from services.api.v1.auth_service.client import grpc_auth_client
from services.api.v1.auth_service.scheme import LoginRequestScheme
from google.protobuf.json_format import MessageToDict
from services.api.v1.auth_service.service import create_access_token
from typing import Annotated
import httpx


auth_service_router = APIRouter(tags=["Auth Service"])


@auth_service_router.post("/auth-login/", response_model=dict)
async def login(
    client: Annotated[auth_pb2_grpc.AuthServiceStub, Depends(grpc_auth_client)],
    request: security.OAuth2PasswordRequestForm = Depends(),
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/user-service/api/v1/get-user-by-username-password/{request.username}/{request.password}/"
        )

    if response.status_code == 200:
        user_data = response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Invalid credentials or external service error",
        )

    access_token = create_access_token(
        data={"sub": user_data.get("user").get("username")}
    )

    return {"access_token": access_token, "token_type": "bearer"}
    # response = await client.Login(
    #     auth_pb2.LoginRequest(
    #         username=request.username,
    #         password=request.password
    #     )
    # )

    # return MessageToDict(response)
