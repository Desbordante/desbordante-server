from typing import Annotated

from fastapi import Depends

from app.dependencies import SessionDep
from app.domain.auth.exceptions import NotAdminException
from app.domain.auth.service import AuthService
from app.domain.user.models import User
from app.domain.user.schemas import UserPublic
from app.repository import BaseRepository

from .tokens import AccessTokenPayloadDep, OptionalAccessTokenPayloadDep


def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(repository=BaseRepository(model=User, session=session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_authorized_user(
    token_data: AccessTokenPayloadDep,
    auth_service: AuthServiceDep,
) -> UserPublic:
    return auth_service.get_by_id(token_data.id)


AuthorizedUserDep = Annotated[UserPublic, Depends(get_authorized_user)]


def get_optionally_authorized_user(
    token_data: OptionalAccessTokenPayloadDep,
    auth_service: AuthServiceDep,
) -> UserPublic | None:
    return auth_service.get_by_id(token_data.id) if token_data else None


OptionallyAuthorizedUserDep = Annotated[
    UserPublic | None, Depends(get_optionally_authorized_user)
]


def get_admin_user(
    token_data: AccessTokenPayloadDep,
    auth_service: AuthServiceDep,
) -> UserPublic:
    if not token_data.is_admin:
        raise NotAdminException()
    return auth_service.get_by_id(token_data.id)


AdminUserDep = Annotated[UserPublic, Depends(get_admin_user)]
