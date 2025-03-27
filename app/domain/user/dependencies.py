from typing import Annotated

from fastapi import Depends

from app.dependencies.dependencies import SessionDep
from app.domain.user.models import User
from app.domain.user.service import UserService
from app.repository.repository import BaseRepository


def get_user_service(session: SessionDep) -> UserService:
    return UserService(repository=BaseRepository(model=User, session=session))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
