from functools import cached_property
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MINIO_HOST: str
    MINIO_PORT: int = 9000
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET: str = "files"
    MINIO_SECURE: bool = False  # Should be True in production
    MINIO_PRESIGNED_URL_EXPIRE_MINUTES: int = 60

    @cached_property
    def minio_endpoint(self) -> str:
        return f"{settings.MINIO_HOST}:{settings.MINIO_PORT}"


settings = Settings()
