from typing import Annotated

from fastapi import Depends

from app.dependencies.dependencies import SessionDep
from app.domain.auth.dependencies import AccessTokenPayloadDep
from app.domain.user.models import User
from app.domain.user.schemas import UserPublic
from app.domain.user.service import UserService
from app.repository.repository import BaseRepository


def get_user_service(session: SessionDep) -> UserService:
    return UserService(repository=BaseRepository(model=User, session=session))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_current_user(
    token_data: AccessTokenPayloadDep,
    user_service: UserServiceDep,
) -> UserPublic:
    return user_service.get_by_id(token_data.id)


CurrentUserDep = Annotated[UserPublic, Depends(get_current_user)]
