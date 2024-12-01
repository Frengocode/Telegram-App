import grpc
from protos import message_pb2_grpc


async def grpc_message_client():
    channel = grpc.aio.insecure_channel("127.0.0.1:50054")
    client = message_pb2_grpc.MessageServiceStub(channel)
    return client
