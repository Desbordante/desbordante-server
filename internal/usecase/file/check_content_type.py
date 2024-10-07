from typing import Protocol

from internal.usecase.file.exception import IncorrectFileFormatException


class File(Protocol):
    content_type: str


class CheckContentType:
    def __call__(self, *, upload_file: File) -> None:
        if (
            upload_file.content_type != "text/csv"
        ):  # TODO: replace with actual validation
            raise IncorrectFileFormatException("File is not CSV")
