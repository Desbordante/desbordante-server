from starsessions.stores.redis import RedisStore

from src.redis.client import client

session_store = RedisStore(connection=client)
