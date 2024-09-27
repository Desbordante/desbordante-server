from pathlib import Path

import aiofiles
import pandas as pd

from internal.dto.repository.file.file import (
    FailedFileReadingException,
    CSVFileFindSchema,
    CSVFileResponseSchema,
)
from internal.dto.repository.file import File, FileCreateSchema
from internal.infrastructure.data_storage.flat import FlatContext

CHUNK_SIZE = 1024


class FileRepository:
    # The current repository implementation does not support transactions.

    async def create(
        self,
        file: File,
        file_info: FileCreateSchema,
        context: FlatContext,
    ) -> None:

        path_to_file = Path.joinpath(
            context.upload_directory_path, str(file_info.file_name)
        )
        try:
            async with aiofiles.open(path_to_file, "wb") as out_file:  # !!!
                while content := await file.read(CHUNK_SIZE):
                    await out_file.write(content)
        except Exception:
            raise FailedFileReadingException("The sent file could not be read.")

    def find(
        self,
        file_info: CSVFileFindSchema,
        context: FlatContext,
    ) -> CSVFileResponseSchema:

        path_to_file = Path(context.upload_directory_path, str(file_info.file_name))

        return pd.read_csv(
            path_to_file,
            sep=file_info.separator,
            header=file_info.header,
        )
