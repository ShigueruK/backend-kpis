import pytest
from httpx import AsyncClient

async def get_admin_token(client):
    response = await client.post(
        "/login",
        data={"username": "admin@example.com", "password": "admin123"}
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_ventas_mensuales_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/ventas-mensuales")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_ventas_mensuales_as_admin(async_client: AsyncClient):
    token = await get_admin_token(async_client)
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/ventas-mensuales", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        # Verifica que tenga las claves esperadas
        assert "mes" in data[0] and "ventas" in data[0] and "objetivo" in data[0]

@pytest.mark.asyncio
async def test_ventas_por_categoria_as_admin(async_client: AsyncClient):
    token = await get_admin_token(async_client)
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/ventas-por-categoria", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "categoria" in data[0] and "ventas" in data[0] and "mes" in data[0] and "anio" in data[0]

async def get_vendedor_token(client):
    response = await client.post(
        "/login",
        data={"username": "vendedor@example.com", "password": "vendedor123"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]
@pytest.mark.asyncio
async def test_ventas_por_categoria_forbidden_for_vendedor(async_client: AsyncClient):
    token = await get_vendedor_token(async_client)
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/ventas-por-categoria", headers=headers)
    assert response.status_code == 403
    pass

