from src.domain.account.tasks import send_confirmation_email


class SendConfirmationEmailUseCase:
    async def __call__(self, to_email: str) -> None:
        send_confirmation_email.delay(to_email=to_email)
