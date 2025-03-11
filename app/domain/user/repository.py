from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
from app.domain.user.exceptions import UserAlreadyExistsException, UserNotFoundException


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> User:
        result = await self._session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException(field="email", value=email)
        return user

    async def get_by_id(self, id: int) -> User:
        result = await self._session.execute(select(User).where(User.id == id))
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException(field="id", value=id)
        return user

    async def add_user(self, user: User) -> User:
        try:
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)
            return user
        except IntegrityError as e:
            raise UserAlreadyExistsException(email=user.email) from e
