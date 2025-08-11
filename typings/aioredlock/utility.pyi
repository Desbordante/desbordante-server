from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar("T")

REDIS_DSN_PATTERN: str

def clean_password(
    details: Union[Dict[str, Any], List[Any], str], cast: Callable[[Any], T] = str
) -> T: ...
