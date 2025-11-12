from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Base rate limits for all routes
    DEFAULT_RATE_LIMIT: str = "100/minute"
    DEFAULT_RATE_LIMIT_HOURLY: str = "1000/hour"

    # Strict limits for auth routes (external API calls)
    AUTH_RATE_LIMIT: str = "10/minute"
    AUTH_RATE_LIMIT_HOURLY: str = "100/hour"

    # Limits for file uploads
    UPLOAD_RATE_LIMIT: str = "20/minute"
    UPLOAD_RATE_LIMIT_HOURLY: str = "200/hour"


settings = Settings()  # type: ignore
