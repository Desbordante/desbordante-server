from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from app.settings import settings

engine = create_engine(url=settings.postgres_dsn.unicode_string())
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
