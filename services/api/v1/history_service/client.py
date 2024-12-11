import grpc
from protos import history_pb2_grpc


async def grpc_history_client():
    channel = grpc.aio.insecure_channel("127.0.0.1:50055")
    client = history_pb2_grpc.HistoryServiceStub(channel)
    return client
