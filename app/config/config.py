from functools import cached_property, lru_cache
from pydantic import AmqpDsn, PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # MinIO settings
    minio_root_user: str
    minio_root_password: str
    minio_default_buckets: str
    minio_host: str
    minio_port: int = 9000

    # Secret key
    secret_key: str

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

    @cached_property
    def minio_dsn(self) -> AnyUrl:
        return AnyUrl.build(
            scheme="http",
            host=self.minio_host,
            port=self.minio_port,
            user=self.minio_root_user,
            password=self.minio_root_password,
        )

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
