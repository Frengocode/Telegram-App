import grpc
from protos import auth_pb2_grpc


async def grpc_auth_client():
    channel = grpc.aio.insecure_channel("127.0.0.1:50052")
    client = auth_pb2_grpc.AuthServiceStub(channel)
    return client
