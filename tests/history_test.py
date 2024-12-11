from tests.confest import get_auth_token
from pathlib import Path
import httpx
import pytest

requests_url = {
    "create_history": "http://localhost:8000/history-service/api/v1/create-history/",
    "get_histories": "http://localhost:8000/history-service/api/v1/get-histories/",
    "get_history": "http://localhost:8000/history-service/api/v1/get-history/",
    "delete_history": "http://localhost:8000/history-service/api/v1/delete-history/",
}


@pytest.mark.asyncio
async def test_create_history():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {"content_title": "Test history"}

    current_dir = Path(__file__).parent
    picture_path = current_dir / "test.jpg"
    assert picture_path.exists(), "File Not found"

    files = {"content": picture_path.open("rb")}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            requests_url["create_history"], files=files, data=data, headers=headers
        )
        assert response.status_code == 200, f"Error of creating data: {response.text}"


@pytest.mark.asyncio
async def test_get_histories():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{requests_url['get_histories']}{3}/", headers=headers
        )
        assert response.status_code == 200, f"Error of getting data: {response.text}"


@pytest.mark.asyncio
async def test_get_history():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    history_id = 1
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{requests_url['get_history']}{history_id}/", headers=headers
        )
        assert response.status_code == 200, f"Error of getting data: {response.text}"


@pytest.mark.asyncio
async def test_delete_history():
    token = await get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    history_id = 1
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{requests_url['delete_history']}{history_id}/", headers=headers
        )
        assert response.status_code == 200, f"Error of deleting data: {response.text}"
