from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4
import aiofiles
from fastapi import APIRouter, Form, HTTPException, UploadFile

from app.domain.file.dataset import DatasetORM
from app.domain.file.file import FileORM
from app.settings import settings

router = APIRouter(prefix="/dataset")


async def save_file(in_file: UploadFile, out_file_path: Path):
    CHUNK_SIZE = 1024
    try:
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await in_file.read(CHUNK_SIZE):
                await out_file.write(content)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to save file")


@router.post("/csv")
async def upload_csv_dataset(
    file: UploadFile,
    separator: Annotated[str, Form()],  # ?separator=","
    header: Annotated[list[int], Form()],  # ?header=0?header=1?header=2
) -> UUID:
    if file.content_type != "text/csv":  # TODO: replace with actual validation
        raise HTTPException(status_code=400, detail="File is not CSV")

    file_name = uuid4()
    path_to_file = Path.joinpath(settings.uploaded_files_dir_path, str(file_name))
    await save_file(file, path_to_file)

    file_orm = FileORM.create(
        mime_type=file.content_type,
        file_name=file_name,
        original_file_name=file.filename,
    )

    dataset_orm = DatasetORM.create(
        separator=separator,
        header=header,
        file=file_orm,
    )

    return dataset_orm.id  # type: ignore
