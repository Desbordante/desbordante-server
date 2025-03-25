from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models import BaseIDModel

if TYPE_CHECKING:
    from app.domain.file.models import File


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    is_admin: bool = Field(default=False)


class User(BaseIDModel, UserBase, table=True):
    hashed_password: str = Field(nullable=False, index=True)
    files: list["File"] = Relationship(back_populates="owner")
