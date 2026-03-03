from dataclasses import dataclass
from typing import Literal, Protocol


class AnonymousActor(Protocol):
    """Anonymous authorization subject."""

    user_id: None
    is_admin: Literal[False]


class AuthenticatedActor(Protocol):
    """Authenticated authorization subject."""

    user_id: int
    is_admin: bool


Actor = AnonymousActor | AuthenticatedActor


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
