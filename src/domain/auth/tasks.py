from datetime import timedelta

from src.domain.auth.config import settings
from src.domain.email.utils import send_email
from src.schemas.email_schemas import ResetPasswordTokenPayloadSchema
from src.worker.worker import worker


@worker.task(name="tasks.send_reset_email")
def send_reset_email(to_email: str) -> None:
    send_email(
        to_email=to_email,
        schema=ResetPasswordTokenPayloadSchema,
        expires_delta=timedelta(minutes=settings.RESET_PASSWORD_EMAIL_EXPIRE_MINUTES),
        subject="Reset your password",
    )
