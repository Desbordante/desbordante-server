# type: ignore
from aioredlock import Aioredlock

from src.infrastructure.redis.client import client

lock_manager = Aioredlock([client])
