import os
from typing import Protocol
from uuid import uuid4

from src.domain.file.config import settings
from src.domain.file.storage import storage
from src.exceptions import TooManyRequestsException
from src.models.file_models import FileModel
from src.models.user_models import UserModel
from src.schemas.file_schemas import File


class FileCrud(Protocol):
    async def create(self, entity: FileModel) -> FileModel: ...
    async def get_temporary_files_size(self, *, owner_id: int) -> int: ...


class UploadFileUseCase:
    def __init__(
        self,
        *,
        file_crud: FileCrud,
        user: UserModel,
    ):
        self.file_crud = file_crud
        self.user = user

    async def __call__(self, *, file: File) -> FileModel:
        temporary_files_size = await self.file_crud.get_temporary_files_size(
            owner_id=self.user.id
        )

        if temporary_files_size + file.size > settings.TEMPORARY_FILES_SIZE_LIMIT:
            raise TooManyRequestsException(
                "Temporary files size limit exceeded. Try again later."
            )

        _, file_extension = os.path.splitext(file.name)
        path = f"{self.user.id}/{uuid4()}{file_extension}"

        await storage.upload_file(file=file, path=path)

        file_entity = FileModel(
            name=file.name,
            size=file.size,
            path=path,
            owner_id=self.user.id,
        )

        try:
            return await self.file_crud.create(entity=file_entity)
        except Exception as e:
            await storage.delete_file(path=path)
            raise e
