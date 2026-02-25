from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    AUTH_SUCCESS_REDIRECT_URL: str

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str


settings = Settings()  # type: ignore
