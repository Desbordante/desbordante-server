from pathlib import Path

import aiofiles
import pandas as pd

from internal.dto.repository.file.file import FailedFileReadingException, CSVFileFindSchema, CSVFileResponseSchema
from internal.infrastructure.data_storage import settings
from internal.dto.repository.file import File, FileCreateSchema, FileResponseSchema
from internal.uow import DataStorageContext

CHUNK_SIZE = 1024

class FileRepository:

    def __init__(self):
        self.files_dir_path = settings.uploaded_files_dir_path

    async def create(
            self,
            file: File,
            file_info: FileCreateSchema,
            context: DataStorageContext  # The current repository implementation does not support transactions.
    ) -> FileResponseSchema:

        path_to_file = Path.joinpath(self.files_dir_path, str(file_info.file_name))
        try:
            async with aiofiles.open(path_to_file, "wb") as out_file: # !!!
                while content := await file.read(CHUNK_SIZE):
                    await out_file.write(content)
        except Exception:
            raise FailedFileReadingException("The sent file could not be read.")


    def find(
            self,
            file_info: CSVFileFindSchema,
            context: DataStorageContext  # The current repository implementation does not support transactions.
    ) -> CSVFileResponseSchema:

        path_to_file = Path(self.files_dir_path, str(file_info.file_name))

        return pd.read_csv(
            path_to_file,
            sep=file_info.separator,
            header=file_info.header,
        )
