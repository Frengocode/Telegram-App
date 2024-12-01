import grpc
from protos import chat_pb2_grpc


async def grpc_chat_client():
    channel = grpc.aio.insecure_channel("127.0.0.1:50053")
    client = chat_pb2_grpc.ChatServiceStub(channel)
    return client
