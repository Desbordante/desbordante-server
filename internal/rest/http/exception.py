from fastapi import FastAPI, Request, HTTPException

from internal.usecase.file.exception import IncorrectFileFormatException, DatasetNotFoundException, \
    FileMetadataNotFoundException
from internal.usecase.task.exception import TaskNotFoundException

def add_exception_handlers(app: FastAPI):

    @app.exception_handler(IncorrectFileFormatException)
    def incorrect_file_format_exception(request: Request, exc: IncorrectFileFormatException):
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


    @app.exception_handler(DatasetNotFoundException)
    def dataset_not_found_exception(request: Request, exc: DatasetNotFoundException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


    @app.exception_handler(FileMetadataNotFoundException)
    def file_metadata_not_found_exception(request: Request, exc: FileMetadataNotFoundException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


    @app.exception_handler(TaskNotFoundException)
    def file_metadata_not_found_exception(request: Request, exc: TaskNotFoundException):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
