from fastapi import status
from tests.confest import get_auth_token, BASE_URL
import pytest
import httpx


@pytest.mark.asyncio
async def test_create_message():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {"message": "Test Message", "chat_id": 3}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/message-service/api/v1/create-message/",
            json=data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
