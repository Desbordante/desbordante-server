from aioredlock import Aioredlock

from src.infrastructure.redis.config import settings

lock_manager = Aioredlock([settings.redis_lock_dsn.unicode_string()])
