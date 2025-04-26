from typing import Annotated

from fastapi import Depends

from _app.dependencies.dependencies import SessionDep
from _app.domain.user.models import User
from _app.domain.user.service import UserService
from _app.repository.repository import BaseRepository


def get_user_service(session: SessionDep) -> UserService:
    return UserService(repository=BaseRepository(model=User, session=session))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
