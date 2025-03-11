from sqlalchemy.ext.asyncio import AsyncAttrs

from app.db.annotations import created_at, updated_at

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
