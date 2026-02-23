from fastapi import Response

from src.domain.session.config import settings


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(settings.SESSION_COOKIE_NAME)


def set_session_cookie(response: Response, session_id: str) -> None:
    response.set_cookie(
        settings.SESSION_COOKIE_NAME,
        session_id,
        httponly=settings.SESSION_COOKIE_HTTP_ONLY,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite=settings.SESSION_COOKIE_SAME_SITE,
        max_age=settings.SESSION_COOKIE_MAX_AGE,
    )
