from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    """Authorization subject."""

    user_id: int | None  # None = anonymous
    is_admin: bool = False
