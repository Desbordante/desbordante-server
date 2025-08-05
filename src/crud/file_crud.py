from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.file_models import FileModel
from src.schemas.file_schemas import FileStatus


class FileFindProps(TypedDict, total=False):
    id: UUID


class FileUpdateProps(TypedDict, total=False):
    pass


class FileCrud(BaseCrud[FileModel, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=FileModel, session=session)

    async def get_by(self, **kwargs: Unpack[FileFindProps]) -> FileModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: FileModel, **kwargs: Unpack[FileUpdateProps]
    ) -> FileModel:
        return await super().update(entity=entity, **kwargs)

    async def get_temporary_files_size(self, *, owner_id: int) -> int:
        query = select(func.sum(self.model.size)).where(
            self.model.status == FileStatus.Temporary,
            self.model.owner_id == owner_id,
        )
        result = await self._session.execute(query)
        return result.scalar() or 0
