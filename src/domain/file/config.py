from functools import cached_property

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MINIO_HOST: str
    MINIO_PORT: int = 9000
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: SecretStr
    MINIO_BUCKET: str = "files"
    MINIO_SECURE: bool = False
    MINIO_PRESIGNED_URL_EXPIRE_MINUTES: int = 60

    TEMPORARY_FILES_SIZE_LIMIT: int = 1024 * 10  # 10KB
    TEMPORARY_FILE_EXPIRE_MINUTES: int = 60

    @cached_property
    def minio_endpoint(self) -> str:
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"


settings = Settings()  # type: ignore
