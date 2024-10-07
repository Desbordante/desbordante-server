import os
from pathlib import Path

import aiofiles

from pydantic import BaseModel

from internal.dto.repository.file import File
from internal.infrastructure.data_storage import settings


CHUNK_SIZE = 1024


class FlatAddModel:
    def __init__(self, file: File, file_name: str):
        self.file_name = file_name
        self.file = file


class FlatDeleteModel(BaseModel):
    file_name: str


class FlatContext:
    def __init__(self, upload_directory_path: Path):
        self._upload_directory_path = upload_directory_path
        self._is_closed = True
        self._to_add: list[FlatAddModel] = []
        self._added: list[Path] = []

    @property
    def upload_directory_path(self) -> Path:
        return self._upload_directory_path

    async def async_flush(self) -> None:
        for file_model in self._to_add:
            path_to_file = Path.joinpath(
                self.upload_directory_path, str(file_model.file_name)
            )
            async with aiofiles.open(path_to_file, "wb") as out_file:
                while content := await file_model.file.read(CHUNK_SIZE):
                    await out_file.write(content)
            self._added.append(path_to_file)
            self._to_add.remove(file_model)

    def flush(self) -> None:
        for file_model in self._to_add:
            path_to_file = Path.joinpath(
                self.upload_directory_path, str(file_model.file_name)
            )
            with open(path_to_file, "wb") as out_file:
                while content := file_model.file.read(CHUNK_SIZE):
                    out_file.write(content)  # type: ignore
            self._added.append(path_to_file)
            self._to_add.remove(file_model)

    def rollback(self) -> None:
        for file_path in self._added:
            if file_path.exists():
                os.remove(file_path)
        self._added.clear()
        self._to_add.clear()

    def commit(self) -> None:
        if self._to_add:
            self.flush()
        self._added.clear()

    def close(self) -> None:
        if self._added:
            self.rollback()
        self._is_closed = True

    def add(self, file_model: FlatAddModel) -> None:
        self._to_add.append(file_model)

    def delete(
        self, file_model: FlatDeleteModel
    ) -> None: ...  # TODO: implement, when needed


class FlatContextMaker:
    def __init__(
        self, *, uploaded_files_dir_path: Path = settings.uploaded_files_dir_path
    ):
        self.uploaded_files_dir_path = uploaded_files_dir_path

    def __call__(self):
        return FlatContext(self.uploaded_files_dir_path)


def get_flat_context_maker(
    *, uploaded_files_dir_path: Path | None = None
) -> FlatContextMaker:
    flat_context_maker = (
        FlatContextMaker(uploaded_files_dir_path=uploaded_files_dir_path)
        if uploaded_files_dir_path
        else FlatContextMaker()
    )
    return flat_context_maker


def get_flat_context() -> FlatContext:
    return get_flat_context_maker()()
