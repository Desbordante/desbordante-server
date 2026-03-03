from dotenv import load_dotenv
from pydantic import ByteSize, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    worker_soft_time_limit_in_seconds: int = Field(default=60, gt=0)
    worker_hard_time_limit_in_seconds: int = Field(default=120, gt=0)
    worker_soft_memory_limit: ByteSize = "2GB"  # type: ignore
    worker_hard_memory_limit: ByteSize = "4GB"  # type: ignore


settings = Settings()  # type: ignore
