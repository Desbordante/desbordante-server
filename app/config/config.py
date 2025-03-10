from functools import cached_property
from dotenv import find_dotenv, load_dotenv
from pydantic import AmqpDsn, PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    # Postgres settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # RabbitMQ settings
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672

    # MinIO settings
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_DEFAULT_BUCKETS: str
    MINIO_HOST: str
    MINIO_PORT: int = 9000

    # Secret key
    SECRET_KEY: str

    @cached_property
    def rabbitmq_url(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.RABBITMQ_DEFAULT_USER,
            password=self.RABBITMQ_DEFAULT_PASS,
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
        )

    @cached_property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @cached_property
    def minio_url(self) -> AnyUrl:
        return AnyUrl.build(
            scheme="http",
            host=self.MINIO_HOST,
            port=self.MINIO_PORT,
            user=self.MINIO_ROOT_USER,
            password=self.MINIO_ROOT_PASSWORD,
        )


settings = Settings()
