import pandas as pd
from fastapi import UploadFile

from _app.domain.file.dataset.models import Dataset
from _app.domain.file.dataset.schemas import DatasetCreate
from _app.domain.file.models import File
from _app.repository.repository import BaseRepository


class DatasetService:
    def __init__(self, repository: BaseRepository[Dataset]):
        self._repository = repository

    def create_dataset(
        self, *, params: DatasetCreate, file: UploadFile, owner_id: int, path: str
    ) -> Dataset:
        df = pd.read_csv(file.file, sep=params.separator)
        columns_count = len(df.columns)
        rows_count = len(df)

        db_dataset = Dataset(
            separator=params.separator,
            has_header=params.has_header,
            columns_count=columns_count,
            rows_count=rows_count,
            file=File(
                name=file.filename,
                byte_size=file.size,
                path=path,
                owner_id=owner_id,
            ),
        )
        dataset = self._repository.create(db_dataset)

        return dataset
