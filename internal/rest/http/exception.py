from fastapi import FastAPI, Request, HTTPException

from internal.usecase.file.exception import (
    IncorrectFileFormatException,
    DatasetNotFoundException,
    FileMetadataNotFoundException,
    FailedReadFileException,
)
from internal.usecase.task.exception import TaskNotFoundException


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(IncorrectFileFormatException)
    def incorrect_file_format_exception(
        request: Request, exc: IncorrectFileFormatException
    ):
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    @app.exception_handler(DatasetNotFoundException)
    def dataset_not_found_exception(_, exc: DatasetNotFoundException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    @app.exception_handler(FileMetadataNotFoundException)
    def file_metadata_not_found_exception(_, exc: FileMetadataNotFoundException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    @app.exception_handler(TaskNotFoundException)
    def task_not_found_exception(_, exc: TaskNotFoundException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    @app.exception_handler(FailedReadFileException)
    def failed_read_file_exception(_, exc: FailedReadFileException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
