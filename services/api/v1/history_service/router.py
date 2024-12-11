from fastapi import APIRouter, Depends, File, UploadFile, Form
from services.api.v1.auth_service.oauth import get_current_user
from protos import history_pb2, history_pb2_grpc
from services.api.v1.history_service.client import grpc_history_client
from uitils.scheme import SUser
from google.protobuf.json_format import MessageToDict


history_service_router = APIRouter(
    tags=["History Service"], prefix="/history-service/api/v1"
)


@history_service_router.post("/create-history/")
async def create_history(
    content_title: str = Form(...),
    content: UploadFile = File(...),
    current_user: SUser = Depends(get_current_user),
    client: history_pb2_grpc.HistoryServiceStub = Depends(grpc_history_client),
):

    file_content = await content.read()

    response = await client.CreateHistory(
        history_pb2.CreateHistoryRequest(
            content_title=content_title,
            content=file_content,
            user_id=int(current_user.id),
        )
    )

    return MessageToDict(response)


@history_service_router.get("/get-histories/{user_id}/")
async def get_historys(
    user_id: int,
    client: history_pb2_grpc.HistoryServiceStub = Depends(grpc_history_client),
    current_user: SUser = Depends(get_current_user),
):
    response = await client.GetHystorys(history_pb2.GetHistorysRequest(user_id=user_id))

    return MessageToDict(response)


@history_service_router.get("/get-history/{id}/")
async def get_history(
    id: int,
    client: history_pb2_grpc.HistoryServiceStub = Depends(grpc_history_client),
    current_user: SUser = Depends(get_current_user),
):
    response = await client.GetHistory(history_pb2.GetHistoryRequest(id=id))

    return MessageToDict(response)


@history_service_router.delete("/delete-history/{id}/")
async def delete_history(
    id: int,
    client: history_pb2_grpc.HistoryServiceStub = Depends(grpc_history_client),
    current_user: SUser = Depends(get_current_user),
):
    response = await client.DeleteHistory(
        history_pb2.DeleteHistoryRequest(id=id, user_id=int(current_user.id))
    )

    return MessageToDict(response)
