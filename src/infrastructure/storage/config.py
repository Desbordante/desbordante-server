from functools import cached_property

from dotenv import load_dotenv
from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MINIO_HOST: str
    MINIO_PORT: int = 9000
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: SecretStr
    MINIO_BUCKET: str = "bucket"
    MINIO_SECURE: bool = False

    @cached_property
    def minio_endpoint_url(self) -> HttpUrl:
        return HttpUrl.build(
            scheme="https" if self.MINIO_SECURE else "http",
            host=self.MINIO_HOST,
            port=self.MINIO_PORT,
        )


settings = Settings()  # type: ignore
