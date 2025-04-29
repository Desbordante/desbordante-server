import logging
import smtplib
from datetime import timedelta
from email.message import EmailMessage
from typing import Type

from src.domain.email.config import settings
from src.domain.security.utils import create_token
from src.schemas.email_schemas import EmailTokenPayloadSchema

logger = logging.getLogger(__name__)


def send_email[T: EmailTokenPayloadSchema](
    to_email: str, schema: Type[T], expires_delta: timedelta, subject: str
) -> None:
    token_pair = create_token(
        schema=schema,
        payload={"email": to_email},
        expires_delta=expires_delta,
    )

    text = token_pair.token

    message = EmailMessage()
    message.set_content(text)
    message["From"] = f"Desbordante <{settings.SMTP_USERNAME}>"
    message["To"] = to_email
    message["Subject"] = subject

    try:
        with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            smtp.login(
                user=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD.get_secret_value(),
            )
            smtp.send_message(msg=message)
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {e}")
        raise e
