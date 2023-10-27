from functools import cache

from .settings import Settings

get_settings = cache(lambda: Settings())
