from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    CONFIRMATION_EMAIL_EXPIRE_MINUTES: int = 10
    STORAGE_LIMIT: int = 1024 * 1024 * 200  # 200Mb


settings = Settings()  # type: ignore
