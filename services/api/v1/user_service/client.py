import grpc
from protos import user_pb2_grpc


async def grpc_user_client():
    channel = grpc.aio.insecure_channel("127.0.0.1:50051")
    client = user_pb2_grpc.UserServiceStub(channel)
    return client
