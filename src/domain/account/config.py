from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    CONFIRMATION_EMAIL_EXPIRE_MINUTES: int = 10
    SMTP_HOST: str
    SMTP_PORT: int = 465
    SMTP_USERNAME: str
    SMTP_PASSWORD: SecretStr


settings = Settings()  # type: ignore
