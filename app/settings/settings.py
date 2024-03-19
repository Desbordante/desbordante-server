from functools import cached_property

from dotenv import load_dotenv, find_dotenv
from pydantic import AmqpDsn, PostgresDsn, Field, ByteSize
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    # Postgres settings
    postgres_dialect_driver: str = "postgresql"
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int = 5432
    # RabbitMQ settings
    rabbitmq_default_user: str
    rabbitmq_default_password: str
    rabbitmq_host: str
    rabbitmq_port: int = 5672
    # Worker limits
    worker_soft_time_limit_in_seconds: int = Field(default=60, gt=0)
    worker_hard_time_limit_in_seconds: int = Field(default=120, gt=0)
    worker_soft_memory_limit: ByteSize = "2GB"
    worker_hard_memory_limit: ByteSize = "4GB"

    @cached_property
    def rabbitmq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.rabbitmq_default_user,
            password=self.rabbitmq_default_password,
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
        )

    @cached_property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=self.postgres_dialect_driver,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )


def get_settings():
    # TODO: create different settings based on environment (production, testing, etc.)
    return Settings()
