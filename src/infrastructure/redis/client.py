from redis.asyncio import Redis
from src.infrastructure.redis.config import settings

client = Redis.from_url(settings.redis_dsn.unicode_string())
