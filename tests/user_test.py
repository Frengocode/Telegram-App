from fastapi import status
from tests.confest import BASE_URL
import pytest
import httpx

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_create_test():
    data = {
        "username":"test",
        "password":"test123312",
        "name":"testingusedra",
        "email":"test@gmail.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/user-service/api/v1/create-user/", json=data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user():
    user_id = 1
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/user-service/api/v1/get-user-by-id/{user_id}/")
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_user_by_username():
    username = "ali"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/user-service/api/v1/get-user/{username}/")
        assert response.status_code == status.HTTP_200_OK



@pytest.mark.asyncio
async def test_get_user_by_usernamme_password():
    data = {
        "username":"ali",
        "password":"admin123321"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/user-service/api/v1/get-user-by-username-password/{data.get("username")}/{data.get("password")}/")
        assert response.status_code == status.HTTP_200_OK


        