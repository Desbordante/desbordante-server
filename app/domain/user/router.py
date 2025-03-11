from fastapi import APIRouter, Depends
from app.domain.user.schemas import UserSchema
from .dependencies import get_current_user

router = APIRouter(
    responses={
        401: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            },
        }
    }
)


@router.get(
    "/me",
    response_model=UserSchema,
    responses={
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        }
    },
    summary="Get current user",
    description="Returns information about the currently authenticated user",
)
async def get_current_user(
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    """
    Get current authenticated user profile

    Returns:
        UserSchema: Current user's profile information

    Raises:
        CredentialsException: When authentication token is invalid
        UserNotFoundException: When user from token not found in database
    """
    return current_user
