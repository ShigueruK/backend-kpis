import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    # Usar form data, no JSON
    response = await async_client.post(
        "/login",
        data={"username": "admin@example.com", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "rol" in data

@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient):
    response = await async_client.post(
        "/login",
        data={"username": "admin@example.com", "password": "wrong"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client: AsyncClient):
    response = await async_client.post(
        "/login",
        data={"username": "fake@example.com", "password": "anything"}
    )
    assert response.status_code == 401