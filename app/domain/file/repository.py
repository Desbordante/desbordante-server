from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .models import File
from .exceptions import FileNotFoundException


class FileRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, file: File) -> File:
        self._session.add(file)
        await self._session.commit()
        await self._session.refresh(file, ["owner"])  # Explicitly load the owner
        return file

    async def get_by_id(self, file_id: UUID) -> File:
        result = await self._session.execute(
            select(File).options(selectinload(File.owner)).where(File.id == file_id)
        )
        file = result.scalars().first()
        if not file:
            raise FileNotFoundException(str(file_id))
        return file

    async def get_user_files(self, user_id: int) -> List[File]:
        result = await self._session.execute(
            select(File)
            .options(selectinload(File.owner))
            .where(File.owner_id == user_id)
        )
        return list(result.scalars().all())

    async def delete(self, file: File) -> None:
        await self._session.delete(file)
        await self._session.commit()
