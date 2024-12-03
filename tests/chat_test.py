from fastapi import status
from tests.confest import BASE_URL, get_auth_token
import httpx
import pytest



@pytest.mark.asyncio
async def test_create_chat():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "member_id" : 4
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/chat-service/api/v1/create-chat/", json=data, headers=headers)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user_chats():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
        response = await client.get(f"{BASE_URL}/chat-service/api/v1/get-user-chats/", headers=headers)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def tets_get_user_chat():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(httpx.Timeout(10.0)) as client:
        response = await client.get(f"{BASE_URL}/chat-service/api/v1/get-user-chat/{3}", headers=headers)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_delete_chat():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/chat-service/api/v1/delete-user-chat/{4}/", headers=headers)
        assert response.status_code == 200







