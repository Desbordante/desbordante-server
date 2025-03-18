from app.exceptions import ResourceNotFoundException, ForbiddenException


class FileNotFoundException(ResourceNotFoundException):
    def __init__(self, file_id: str):
        super().__init__(f"File with id {file_id} not found")


class FileAccessDeniedException(ForbiddenException):
    def __init__(self):
        super().__init__("You don't have permission to access this file")
