from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, status
from app.domain.user.dependencies import get_current_user
from app.domain.user.schemas import UserSchema
from .dependencies import get_file_service
from .service import FileService
from .schemas import FileSchema

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            },
        }
    },
)


@router.post(
    "/",
    response_model=FileSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file",
    description="Upload a file to the server. The file will be associated with the current user.",
)
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserSchema = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> FileSchema:
    """
    Upload a new file:
    - Validates user authentication
    - Stores file in MinIO
    - Creates database record
    - Returns file metadata with download URL
    """
    return await file_service.upload_file(file, current_user.id)


@router.get(
    "/{file_id}",
    response_model=FileSchema,
    responses={
        404: {"description": "File not found"},
        403: {"description": "Access denied"},
    },
    summary="Get file details",
    description="Get file metadata and generate a presigned download URL.",
)
async def get_file(
    file_id: UUID,
    current_user: UserSchema = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> FileSchema:
    """
    Get file details:
    - Validates user authentication and ownership
    - Generates presigned download URL
    - Returns file metadata with download URL
    """
    return await file_service.get_file(file_id, current_user.id)


@router.get(
    "/",
    response_model=List[FileSchema],
    summary="List user files",
    description="Get a list of all files uploaded by the current user.",
)
async def list_files(
    current_user: UserSchema = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> List[FileSchema]:
    """
    List all files:
    - Returns list of files owned by current user
    - Includes metadata and download URLs
    """
    return await file_service.get_user_files(current_user.id)


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "File not found"},
        403: {"description": "Access denied"},
    },
    summary="Delete a file",
    description="Delete a file from the server. Only the file owner can delete it.",
)
async def delete_file(
    file_id: UUID,
    current_user: UserSchema = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
):
    """
    Delete a file:
    - Validates user authentication and ownership
    - Removes file from MinIO storage
    - Deletes database record
    """
    await file_service.delete_file(file_id, current_user.id)
    return None
