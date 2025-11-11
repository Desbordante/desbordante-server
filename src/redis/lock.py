# type: ignore
from aioredlock import Aioredlock

from src.redis.client import client

lock_manager = Aioredlock([client])
