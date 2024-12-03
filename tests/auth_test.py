from fastapi import status, security, Depends
from tests.confest import BASE_URL
import pytest
import httpx



@pytest.mark.asyncio
async def test_login():
    data = {
        "username": "ali",
        "password": "admin123321"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/auth-login/", json=data)
        assert response.status_code == status.HTTP_200_OK


    

    #### Add cache for get-user-by-id
    ### update profile picture
    ### update profile components
    ### delete message and more