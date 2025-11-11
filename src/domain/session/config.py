from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    COOKIE_NAME: str = "session_id"
    COOKIE_HTTPS_ONLY: bool = True
    LIFETIME: int = 3600 * 24 * 30  # 30 days
    ROLLING: bool = True
    PREFIX: str = "session:"


settings = Settings()  # type: ignore
