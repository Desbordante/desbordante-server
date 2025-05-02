from typing import List
from uuid import UUID

from fastapi import APIRouter, File, UploadFile, status, Query

from app.domain.auth.dependencies import AuthorizedUserDep
from app.domain.auth.dependencies.auth import OptionallyAuthorizedUserDep
from app.exceptions.exceptions import ForbiddenException

from .dependencies import FileServiceDep
from .models import FilePublic, FileFull

router = APIRouter()


@router.post(
    "",
    response_model=FilePublic,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file",
    description="Upload a file to the server. The file will be associated with the current user.",
)
def upload_file(
    user: AuthorizedUserDep,
    file_service: FileServiceDep,
    file: UploadFile = File(),
    make_public: bool = False,
) -> FilePublic:
    """
    Upload a new file:
    - Validates user authentication
    - Stores file in MinIO
    - Creates database record
    - Returns file metadata
    """
    if make_public and not user.is_admin:
        raise ForbiddenException("Access denied")

    return file_service.upload_file(file, user.id if not make_public else None)


@router.get(
    "/ids",
    response_model=List[FileFull],
    summary="List user files",
    description="Get a list of all files uploaded by the current user.",
)
def get_file_by_id(
    #user: OptionallyAuthorizedUserDep,
    file_service: FileServiceDep,
    ids: List[UUID] = Query([]),
) -> List[FileFull]:
    """
    List all files:
    - Returns list of files owned by current user
    - Includes metadata and download URLs
    """
    import pandas as pd
    from io import BytesIO
    from app.domain.storage import storage

    print(999, ids)

    files = [file_service.get_file_by_id(id) for id in ids]
    print("!!!!!!!!!!!!")
    full_files = []
    for file in files:
        table = pd.read_csv(BytesIO(storage.download_file(file.path)))
        extra_info = {
            'num_columns': len(table.columns),
            'num_rows': len(table),
            'with_header': True,
            'header': table.columns,
        }
        full_files.append(FileFull(**file.model_dump(), **extra_info))

    return full_files


@router.get(
    "",
    response_model=List[FilePublic],
    summary="List user files",
    description="Get a list of all files uploaded by the current user.",
)
def get_my_files(
    user: OptionallyAuthorizedUserDep,
    file_service: FileServiceDep,
    with_public: bool = True,
) -> List[FilePublic]:
    """
    List all files:
    - Returns list of files owned by current user
    - Includes metadata and download URLs
    """

    user_files = file_service.get_user_files(user.id) if user else []
    public_files = file_service.get_public_files() if with_public else []

    return user_files + public_files
