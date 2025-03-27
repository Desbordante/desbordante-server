from fastapi import APIRouter

from app.domain.auth.dependencies import AuthorizedUserDep
from app.domain.user.schemas import UserPublic

router = APIRouter()


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Get current user",
    description="Returns information about the currently authenticated user",
)
def get_current_user(
    current_user: AuthorizedUserDep,
) -> UserPublic:
    """
    Get current authenticated user profile

    Returns:
        UserSchema: Current user's profile information

    Raises:
        CredentialsException: When authentication token is invalid
        UserNotFoundException: When user from token not found in database
    """
    return current_user
