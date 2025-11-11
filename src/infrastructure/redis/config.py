from functools import cached_property

from dotenv import load_dotenv
from pydantic import RedisDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    @cached_property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )


settings = Settings()  # type: ignore
