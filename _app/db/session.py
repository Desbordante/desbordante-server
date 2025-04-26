from typing import Generator

from sqlmodel import Session, create_engine

from _app.config import settings
from _app.domain.user.models import User  # noqa: F401

engine = create_engine(settings.postgres_dsn.unicode_string(), echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
