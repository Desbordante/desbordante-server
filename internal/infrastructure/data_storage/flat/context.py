from pathlib import Path

from internal.infrastructure.data_storage import settings


class FlatContext:

    def __init__(self, upload_directory_path: Path):
        self._upload_directory_path = upload_directory_path

    @property
    def upload_directory_path(self) -> Path:
        return self._upload_directory_path

    # This context implementation does not support transactions
    def flush(self) -> None: ...

    def rollback(self) -> None: ...

    def commit(self) -> None: ...

    def close(self) -> None: ...  # TODO: implement flat context closing.


class FlatContextMaker:

    def __call__(self):
        return FlatContext(settings.uploaded_files_dir_path)


def get_flat_context_maker() -> FlatContextMaker:
    return FlatContextMaker()
