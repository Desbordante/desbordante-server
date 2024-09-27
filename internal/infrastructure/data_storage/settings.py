# type: ignore

# Values ​​in the settings are added dynamically, so the static analyzer,
# without knowing this, produces an error.

from functools import cached_property

from dotenv import load_dotenv, find_dotenv
from pydantic import AmqpDsn, DirectoryPath, PostgresDsn
from pydantic_settings import BaseSettings
from pathlib import Path

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
    # Flat files settings
    uploaded_files_dir_path: DirectoryPath = Path("uploads/")

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
