from typing import Protocol

from src.exceptions import IncorrectFileFormatException


class File(Protocol):
    content_type: str


class CheckContentTypeUseCase:
    def __call__(self, *, file: File) -> None:
        if file.content_type != "text/csv":  # TODO: replace with actual validation
            raise IncorrectFileFormatException("File is not CSV")
