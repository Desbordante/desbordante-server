import json
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Annotated, Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from sqlalchemy import JSON, Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.type_api import TypeEngine


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


class ApiErrorSchema(BaseSchema):
    detail: str


class OptionalSchema(BaseSchema):
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


class PydanticType(TypeDecorator[Any]):
    """Pydantic type for SQLAlchemy.
    Inspired by: https://gist.github.com/imankulov/4051b7805ad737ace7d8de3d3f934d6b,
                 https://gist.github.com/a1d4r/100b06239925a414446305c81433cc88
    SAVING:
    - Uses JSON type under the hood.
    - Acceps the pydantic model and converts it to a dict on save.
    - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
    - Pulls the string from the database.
    - SQLAlchemy engine JSON-decodes the string to a dict.
    - Uses the dict to create a pydantic model.
    """

    cache_ok = True
    impl = JSONB

    def __init__(self, model_type: Any) -> None:
        super().__init__()
        self.model_type = model_type
        self._adapter = TypeAdapter(model_type)

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())

    def process_bind_param(self, value: Any, dialect: Dialect) -> Any:
        return jsonable_encoder(value) if value else None

    def process_result_value(self, value: Any, dialect: Dialect) -> Any:
        if value is not None:
            return self._adapter.validate_python(value)
        return None


class PaginationParamsSchema(BaseSchema):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class OrderingDirection(StrEnum):
    Asc = auto()
    Desc = auto()


class OrderingParamsSchema[T: str](BaseSchema):
    order_by: T | None = None
    direction: OrderingDirection = OrderingDirection.Desc


class FiltersParamsSchema(BaseSchema):
    search: str | None = ""


class QueryParamsSchema[T: FiltersParamsSchema, U: str](BaseSchema):
    filters: Annotated[T, Depends()]
    ordering: Annotated[OrderingParamsSchema[U], Depends()]


class TaskStatus(StrEnum):
    Pending = auto()
    Processing = auto()
    Success = auto()
    Failed = auto()


class TaskErrorSchema(BaseSchema):
    error: str


@dataclass
class PaginatedResult[T]:
    total_count: int
    limit: int
    offset: int
    items: list[T]


class PaginatedResponseSchema[T: BaseSchema](BaseSchema):
    total_count: int
    limit: int
    offset: int
    items: list[T]
