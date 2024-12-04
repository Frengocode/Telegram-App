from fastapi import status
from tests.confest import BASE_URL, get_auth_token
from pathlib import Path
import pytest
import httpx


BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_create_user():
    data = {
        "username": "asdas",
        "password": "test123312",
        "name": "testingusedra",
        "email": "test@gmail.com",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/user-service/api/v1/create-user/", json=data
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user():
    user_id = 1
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user-service/api/v1/get-user-by-id/{user_id}/"
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user_by_username():
    username = "ali"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user-service/api/v1/get-user/{username}/"
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user_by_usernamme_password():
    data = {"username": "ali", "password": "admin123321"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/user-service/api/v1/get-user-by-username-password/{data.get("username")}/{data.get("password")}/"
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_user_profile():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    data = {"username": "ali", "name": "string", "email": "string", "surname": "string"}

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{BASE_URL}/user-service/api/v1/update-user-profile/",
            json=data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_profile_picture():

    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    current_dir = Path(__file__).parent
    picture_path = current_dir / "test.jpg"

    files = {"profile_picture": picture_path.open("rb")}

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{BASE_URL}/user-service/api/v1/update-profile-picture/",
            files=files,
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK
