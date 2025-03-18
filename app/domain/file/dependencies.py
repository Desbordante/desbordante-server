from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from .repository import FileRepository
from .service import FileService


async def get_file_service(session: AsyncSession = Depends(get_session)) -> FileService:
    return FileService(repository=FileRepository(session=session))
