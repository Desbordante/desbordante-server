from slowapi import Limiter
from slowapi.util import get_remote_address

from src.infrastructure.rate_limit.config import settings
from src.infrastructure.redis.config import settings as redis_settings

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_settings.redis_rate_limit_dsn.unicode_string(),
    default_limits=[settings.DEFAULT_RATE_LIMIT, settings.DEFAULT_RATE_LIMIT_HOURLY],
)
