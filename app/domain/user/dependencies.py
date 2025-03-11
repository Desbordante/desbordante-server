from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.domain.user.repository import UserRepository
from app.domain.user.schemas import UserSchema
from app.domain.user.service import UserService
from app.domain.auth.dependencies import get_access_token_data


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(repository=UserRepository(session=session))


async def get_current_user(
    token_data=Depends(get_access_token_data),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    return await user_service.get_by_id(token_data.id)
