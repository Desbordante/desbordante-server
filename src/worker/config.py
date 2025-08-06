from functools import cached_property

from dotenv import load_dotenv
from pydantic import AmqpDsn, SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: SecretStr
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672

    @cached_property
    def rabbitmq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.RABBITMQ_DEFAULT_USER,
            password=self.RABBITMQ_DEFAULT_PASS.get_secret_value(),
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
        )


settings = Settings()  # type: ignore
