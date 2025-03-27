from typing import Generator

from sqlmodel import Session, create_engine

from app.config import settings
from app.domain.user.models import User  # noqa: F401

engine = create_engine(settings.postgres_dsn.unicode_string(), echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
