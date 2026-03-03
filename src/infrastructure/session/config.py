from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SESSION_COOKIE_NAME: str = "session_id"
    SESSION_COOKIE_HTTP_ONLY: bool = True
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_SAME_SITE: Literal["lax", "strict", "none"] = "lax"
    SESSION_COOKIE_MAX_AGE: int = 3600 * 24 * 30  # 30 days
    SESSION_ROLLING_LIFETIME: int = 3600 * 24  # 24 hours
    SESSION_ABSOLUTE_LIFETIME: int = 3600 * 24 * 30  # 30 days
    SESSION_KEY_PREFIX: str = "session"
    SESSION_INDEX_KEY_PREFIX: str = "user_sessions"
    SESSION_TOKEN_BYTES: int = 32  # 32 bytes


settings = Settings()  # type: ignore
