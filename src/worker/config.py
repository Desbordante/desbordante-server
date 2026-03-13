from functools import cached_property

from dotenv import load_dotenv
from pydantic import AmqpDsn, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: SecretStr
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    @cached_property
    def rabbitmq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.RABBITMQ_DEFAULT_USER,
            password=self.RABBITMQ_DEFAULT_PASS.get_secret_value(),
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
        )

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
