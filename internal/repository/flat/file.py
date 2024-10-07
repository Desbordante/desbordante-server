from pathlib import Path

import pandas as pd

from internal.dto.repository.file.file import (
    FailedFileReadingException,
    CSVFileFindSchema,
    CSVFileResponseSchema,
)
from internal.dto.repository.file import File, FileCreateSchema
from internal.infrastructure.data_storage.flat import FlatAddModel
from internal.infrastructure.data_storage import Context


class FileRepository:
    async def create(
        self,
        file: File,
        file_info: FileCreateSchema,
        context: Context,
    ) -> None:
        model = FlatAddModel(file=file, file_name=str(file_info.file_name))

        try:
            context.add(model)
            await context.async_flush()
        except Exception:
            raise FailedFileReadingException("The sent file could not be read.")

    def find(
        self,
        file_info: CSVFileFindSchema,
        context: Context,
    ) -> CSVFileResponseSchema:
        path_to_file = Path(
            context.flat_context.upload_directory_path, str(file_info.file_name)
        )

        return pd.read_csv(
            path_to_file,
            sep=file_info.separator,
            header=file_info.header,
        )
