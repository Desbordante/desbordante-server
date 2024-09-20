
from dotenv import load_dotenv, find_dotenv
from pydantic import Field, ByteSize
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    # Celery worker limits
    worker_soft_time_limit_in_seconds: int = Field(default=60, gt=0)
    worker_hard_time_limit_in_seconds: int = Field(default=120, gt=0)
    worker_soft_memory_limit: ByteSize = "2GB"
    worker_hard_memory_limit: ByteSize = "4GB"


def get_settings():
    # TODO: create different settings based on environment (production, testing, etc.)
    return Settings()
