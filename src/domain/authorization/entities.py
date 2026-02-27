from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    """Authorization subject."""

    user_id: int | None  # None = anonymous
    is_admin: bool = False


@dataclass(frozen=True)
class Dataset:
    """Dataset authorization entity."""

    owner_id: int
    is_public: bool


@dataclass(frozen=True)
class Task:
    """Task authorization entity."""

    owner_id: int
    is_public: bool


@dataclass(frozen=True)
class User:
    """User authorization entity."""

    id: int
    is_admin: bool
