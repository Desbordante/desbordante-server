from functools import cached_property

from dotenv import load_dotenv, find_dotenv
from pydantic import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    postgres_dialect_driver: str = "postgresql"

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int = 5432

    rabbitmq_default_user: str
    rabbitmq_default_password: str
    rabbitmq_host: str
    rabbitmq_port: int = 5672

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
