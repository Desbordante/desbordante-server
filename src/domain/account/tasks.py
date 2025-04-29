from datetime import timedelta

from celery import shared_task

from src.domain.account.config import settings
from src.domain.email.utils import send_email
from src.schemas.email_schemas import ConfirmationTokenPayloadSchema


@shared_task
def send_confirmation_email(to_email: str) -> None:
    send_email(
        to_email=to_email,
        schema=ConfirmationTokenPayloadSchema,
        expires_delta=timedelta(minutes=settings.CONFIRMATION_EMAIL_EXPIRE_MINUTES),
        subject="Confirm your email",
    )
