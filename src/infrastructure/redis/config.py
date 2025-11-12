from functools import cached_property

from dotenv import load_dotenv
from pydantic import RedisDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    REDIS_SESSIONS_DB: int = 0
    REDIS_RATE_LIMIT_DB: int = 1
    REDIS_LOCK_DB: int = 2

    @cached_property
    def redis_sessions_dsn(self) -> RedisDsn:
        """Redis DSN for sessions."""
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=str(self.REDIS_SESSIONS_DB),
        )

    @cached_property
    def redis_rate_limit_dsn(self) -> RedisDsn:
        """Redis DSN for rate limiting."""
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=str(self.REDIS_RATE_LIMIT_DB),
        )

    @cached_property
    def redis_lock_dsn(self) -> RedisDsn:
        """Redis DSN for locks."""
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=str(self.REDIS_LOCK_DB),
        )


settings = Settings()  # type: ignore
