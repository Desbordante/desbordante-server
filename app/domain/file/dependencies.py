from typing import Annotated

from fastapi import Depends

from app.dependencies.dependencies import SessionDep
from app.domain.file.models import File
from app.domain.file.service import FileService
from app.repository.repository import BaseRepository


def get_file_service(session: SessionDep) -> FileService:
    return FileService(repository=BaseRepository(model=File, session=session))


FileServiceDep = Annotated[FileService, Depends(get_file_service)]
