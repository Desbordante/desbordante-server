from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.models import BaseIDModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    is_admin: bool = Field(default=False)


class User(BaseIDModel, UserBase, table=True):
    hashed_password: str = Field(nullable=False, index=True)
