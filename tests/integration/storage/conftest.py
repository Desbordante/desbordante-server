from typing import Callable

import pytest
import pytest_asyncio
from moto.server import ThreadedMotoServer

from src.infrastructure.storage.client import S3Storage

from .constants import TEST_BUCKET
from .helpers import make_file as make_file_helper


@pytest.fixture(scope="function")
def moto_server():
    """Start moto S3 mock server. State is cleared when server stops."""
    server = ThreadedMotoServer(port=0)
    try:
        server.start()
        host, port = server.get_host_and_port()
        yield f"http://{host}:{port}"
    finally:
        server.stop()


@pytest_asyncio.fixture(scope="function")
async def s3_storage(moto_server: str) -> S3Storage:
    """S3 storage using moto mock server. No cleanup needed — server state is fresh per test."""
    storage = S3Storage(
        endpoint_url=moto_server,
        access_key="testing",
        secret_key="testing",
        bucket=TEST_BUCKET,
    )
    async with storage.get_client() as client:
        await client.create_bucket(Bucket=TEST_BUCKET)
    return storage


@pytest.fixture
def make_file() -> Callable[..., object]:
    """Factory for File-protocol compatible objects."""
    return make_file_helper
