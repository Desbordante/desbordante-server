from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    RESET_PASSWORD_EMAIL_EXPIRE_MINUTES: int = 10

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str


settings = Settings()  # type: ignore
