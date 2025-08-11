import logging
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from aioredlock.errors import LockAcquiringError as LockAcquiringError
from aioredlock.errors import LockError as LockError
from aioredlock.errors import LockRuntimeError as LockRuntimeError
from aioredlock.sentinel import Sentinel as Sentinel
from aioredlock.utility import clean_password as clean_password

def all_equal(iterable: Iterable[Any]) -> bool: ...
def raise_error(results: List[Any], default_message: str) -> None: ...

class Instance:
    SET_LOCK_SCRIPT: str
    UNSET_LOCK_SCRIPT: str
    GET_LOCK_TTL_SCRIPT: str
    connection: Union[Dict[str, Any], str, Tuple[str, int], Sentinel]
    set_lock_script_sha1: Optional[str]
    unset_lock_script_sha1: Optional[str]
    get_lock_ttl_script_sha1: Optional[str]

    def __init__(
        self, connection: Union[Dict[str, Any], str, Tuple[str, int], Sentinel]
    ) -> None: ...
    @property
    def log(self) -> logging.Logger: ...
    async def connect(self) -> None: ...
    async def close(self) -> None: ...
    async def set_lock(
        self,
        resource: str,
        lock_identifier: str,
        lock_timeout: float,
        register_scripts: bool = False,
    ) -> float: ...
    async def get_lock_ttl(
        self, resource: str, lock_identifier: str, register_scripts: bool = False
    ) -> int: ...
    async def unset_lock(
        self, resource: str, lock_identifier: str, register_scripts: bool = False
    ) -> bool: ...
    async def is_locked(self, resource: str) -> bool: ...

class Redis:
    instances: List[Instance]

    def __init__(
        self,
        redis_connections: List[Union[Dict[str, Any], str, Tuple[str, int], Sentinel]],
    ) -> None: ...
    @property
    def log(self) -> logging.Logger: ...
    async def set_lock(
        self, resource: str, lock_identifier: str, lock_timeout: float = 10.0
    ) -> float: ...
    async def get_lock_ttl(
        self, resource: str, lock_identifier: Optional[str] = None
    ) -> int: ...
    async def unset_lock(self, resource: str, lock_identifier: str) -> bool: ...
    async def is_locked(self, resource: str) -> bool: ...
    async def clear_connections(self) -> None: ...
