from datetime import datetime
from types import get_original_bases
from typing import Any, get_args, get_origin

from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.db.annotations import created_at, updated_at, uuid_pk
from src.schemas.base_schemas import PydanticType, TaskErrorSchema, TaskStatus


def _get_result_type(cls: Any) -> type:
    """Extract result type from BaseTaskModel[T] inheritance."""
    for base in get_original_bases(cls):
        if get_origin(base) is BaseTaskModel:
            args = get_args(base)
            if args:
                return args[0]
    raise TypeError(f"{cls.__name__} must inherit from BaseTaskModel[SomeType]")


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class BaseTaskModel[T](BaseModel):
    """Base model for Celery tasks with generic result type."""

    __abstract__ = True

    id: Mapped[uuid_pk]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=TaskStatus.PENDING,
    )

    @declared_attr
    def result(cls) -> Mapped[T | TaskErrorSchema | None]:
        result_type = _get_result_type(cls)
        return mapped_column(
            PydanticType(result_type | TaskErrorSchema | None),
            default=None,
        )

    finished_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
