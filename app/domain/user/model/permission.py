from enum import auto
from enum import StrEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class AllPermissions(StrEnum):
    CAN_USE_BUILTIN_DATASETS = auto()
    CAN_USE_OWN_DATASETS = auto()
    CAN_USE_USERS_DATASETS = auto()
    CAN_VIEW_ADMIN_INFO = auto()
    CAN_MANAGE_USERS_SESSIONS = auto()
    CAN_MANAGE_APP_CONFIG = auto()


class Permission(Base):
    __tablename__ = "Permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    permission: Mapped[AllPermissions]
