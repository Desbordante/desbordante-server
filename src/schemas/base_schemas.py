import json
from enum import StrEnum, auto
from typing import Annotated, Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    def serializable_dict(self):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)

    def __json__(self):
        """Make BaseSchema objects JSON serializable by default."""
        return self.serializable_dict()


class ApiErrorSchema(BaseSchema):
    detail: str


class OptionalSchema(BaseModel):
    """
    A base model class that automatically sets all fields, except those defined in
    `__non_optional_fields__`, to `None` by default. This allows for the creation
    of model where fields are optional unless explicitly marked as required.

    Attributes:
        __non_optional_fields__ (set): A set of field names that should remain
        non-optional. Fields listed here will not have `None` as their default value.
    """

    __non_optional_fields__: set[str] = set()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """
        Class-level initializer that ensures all fields except those specified
        in `__non_optional_fields__` are set to `None` by default. This method
        is called during the subclass initialization process.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass initializer.
        Exceptions:
            ValueError: If a field listed in `__non_optional_fields__` has a default value of `None`.
        """
        super().__pydantic_init_subclass__(**kwargs)

        for field_name, value in cls.model_fields.items():
            if field_name in cls.__non_optional_fields__:
                if value.default is None:
                    raise ValueError(
                        f"Field '{field_name}' is in __non_optional_fields__ but has a default value of None."
                    )
                continue
            value.default = None

        cls.model_rebuild(force=True)


class PaginationParamsSchema(BaseSchema):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class OrderingDirection(StrEnum):
    Asc = auto()
    Desc = auto()


class OrderingParamsSchema[T: str](BaseSchema):
    order_by: T | None = None
    direction: OrderingDirection = OrderingDirection.Desc


class QueryParamsSchema[T, U: str](BaseSchema):
    search: str | None = None
    filters: Annotated[T, Depends()]
    ordering: Annotated[OrderingParamsSchema[U], Depends()]


class TaskStatus(StrEnum):
    Pending = auto()
    Processing = auto()
    Success = auto()
    Failed = auto()


# JSON encoder and monkey patch for BaseSchema objects
class BaseSchemaJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles BaseSchema objects."""

    def default(self, o: Any) -> Any:
        if isinstance(o, BaseSchema):
            return o.serializable_dict()
        return super().default(o)


# Monkey patch the default json encoder to use our custom encoder
_original_dumps = json.dumps


def custom_dumps(*args: Any, **kwargs: Any) -> str:
    """Custom json.dumps that uses BaseSchemaJSONEncoder by default."""
    if "cls" not in kwargs:
        kwargs["cls"] = BaseSchemaJSONEncoder
    return _original_dumps(*args, **kwargs)


json.dumps = custom_dumps
