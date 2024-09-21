from pathlib import Path

from internal.infrastructure.data_storage import settings


class FlatContext:

    def __init__(self, upload_directory_path: Path):
        self._upload_directory_path = upload_directory_path

    @property
    def upload_directory_path(self) -> Path:
        return self._upload_directory_path

    # This context implementation does not support transactions
    def flush(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def close(self) -> None:
        pass  # TODO: implement flat context closing.


class FlatContextMaker:

    def __call__(self):
        return FlatContext(settings.uploaded_files_dir_path)
