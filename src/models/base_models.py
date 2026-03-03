from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr

from src.db.annotations import created_at, updated_at


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower().replace('model', '')}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
