from typing import Annotated
from uuid import UUID

from fastapi import Form, UploadFile, Depends, APIRouter

from internal.rest.http.file.di import (
    get_save_file_use_case,
    get_save_dataset_use_case,
    get_check_content_type_use_case,
)
from internal.usecase.file import SaveFile, SaveDataset, CheckContentType

router = APIRouter()


class UploadFileAdapter:
    def __init__(self, upload_file: UploadFile):
        self.filename = upload_file.filename or ""
        self.content_type = upload_file.content_type or ""
        self._upload_file = upload_file

    async def read(self, chunk_size: int) -> bytes:
        return await self._upload_file.read(chunk_size)


@router.post("/csv")
async def upload_csv_dataset(
    file: UploadFile,
    separator: Annotated[str, Form()],  # ?separator=","
    header: Annotated[list[int], Form()],  # ?header=0?header=1?header=2,
    check_content_type: CheckContentType = Depends(get_check_content_type_use_case),
    save_file: SaveFile = Depends(get_save_file_use_case),
    save_dataset: SaveDataset = Depends(get_save_dataset_use_case),
) -> UUID:

    adapted_file = UploadFileAdapter(file)

    check_content_type(upload_file=adapted_file)
    save_file_result = await save_file(upload_file=adapted_file)
    save_dataset_result = save_dataset(
        file_id=save_file_result.id,
        separator=separator,
        header=header,
    )
    return save_dataset_result
