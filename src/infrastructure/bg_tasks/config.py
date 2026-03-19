from functools import cached_property

from dotenv import load_dotenv
from pydantic import ByteSize, Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    worker_soft_time_limit_in_seconds: int = Field(default=60, gt=0)
    worker_hard_time_limit_in_seconds: int = Field(default=120, gt=0)
    worker_soft_memory_limit: ByteSize = "2GB"  # type: ignore
    worker_hard_memory_limit: ByteSize = "4GB"  # type: ignore

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    @cached_property
    def database_url(self) -> str:
        """Sync PostgreSQL URL for Celery DatabaseBackend (SQLAlchemy: postgresql+psycopg)."""
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD.get_secret_value(),
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


settings = Settings()  # type: ignore
