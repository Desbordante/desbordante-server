import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_ping(client: AsyncClient):
    response = await client.get("/ping")

    assert response.status_code == 200
    assert response.json() == "Pong!"
