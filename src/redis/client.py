from redis.asyncio import Redis
from src.redis.config import settings

client = Redis.from_url(settings.redis_dsn.unicode_string())
