import ssl
from typing import Any, Dict, Optional, Tuple, Union

class SentinelConfigError(Exception): ...

class Sentinel:
    master: Optional[str]
    connection: Union[Dict[str, Any], str, Tuple[str, int]]
    redis_kwargs: Dict[str, Any]

    def __init__(
        self,
        connection: Union[Dict[str, Any], str, Tuple[str, int]],
        master: Optional[str] = None,
        password: Optional[str] = None,
        db: Optional[int] = None,
        ssl_context: Optional[Union[ssl.SSLContext, bool]] = None,
    ) -> None: ...
    async def get_sentinel(self) -> Any: ...
    async def get_master(self) -> Any: ...
