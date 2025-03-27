from typing import List

from fastapi import APIRouter, File, UploadFile, status

from app.domain.auth.dependencies import AuthorizedUserDep

from .dependencies import FileServiceDep
from .models import FilePublic

router = APIRouter()


@router.post(
    "/",
    response_model=FilePublic,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file",
    description="Upload a file to the server. The file will be associated with the current user.",
)
def upload_file(
    current_user: AuthorizedUserDep,
    file_service: FileServiceDep,
    file: UploadFile = File(),
) -> FilePublic:
    """
    Upload a new file:
    - Validates user authentication
    - Stores file in MinIO
    - Creates database record
    - Returns file metadata
    """
    return file_service.upload_file(file, current_user.id)


@router.get(
    "/",
    response_model=List[FilePublic],
    summary="List user files",
    description="Get a list of all files uploaded by the current user.",
)
def get_my_files(
    current_user: AuthorizedUserDep,
    file_service: FileServiceDep,
) -> List[FilePublic]:
    """
    List all files:
    - Returns list of files owned by current user
    - Includes metadata and download URLs
    """
    return file_service.get_user_files(current_user.id)
