# type: ignore
from aioredlock import Aioredlock

from src.redis.config import settings

lock_manager = Aioredlock([settings.redis_dsn.unicode_string()])
