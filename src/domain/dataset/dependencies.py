from src.infrastructure.storage.client import S3Storage
from src.infrastructure.storage.client import get_storage as create_storage


async def get_storage() -> S3Storage:
    return create_storage()
