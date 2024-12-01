from protos import auth_pb2_grpc, auth_pb2
from uitils.utils import create_access_token
import httpx
import asyncio
import grpc
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class AuthService(auth_pb2_grpc.AuthServiceServicer):

    async def Login(self, request, context):
        user_data = await self.get_data_from_url(
            f"http://localhost:8000/user-service/api/v1/get-user-by-username-password/{request.username}/{request.password}/"
        )

        if user_data is not None:
            log.info("User Not Found")
            token = create_access_token(
                data={"sub": user_data.get("user").get("username")}
            )

            return auth_pb2.LoginResponse(access_token=token, token_type="bearer")

    async def get_data_from_url(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}")
            if response is not None:
                return response.json()
            return None


async def auth_run(addr="localhost:50052"):
    server = grpc.aio.server()

    auth_service = AuthService()

    auth_pb2_grpc.add_AuthServiceServicer_to_server(auth_service, server)
    server.add_insecure_port(addr)

    log.warning(f"Starting server on {addr}")
    await server.start()
    await server.wait_for_termination()
    log.error("Error while starting the server:")


if __name__ == "__main__":
    asyncio.run(auth_run())
