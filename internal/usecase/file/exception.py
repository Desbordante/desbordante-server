class IncorrectFileFormatException(Exception):
    """
    Exception raised when a file format is incorrect or not supported.
    """

    def __init__(self, message: str):
        """
        Initializes an instance of IncorrectFileFormatException with a specific error message.

        Args:
            message(str): The error message to be reported.
        """
        super().__init__(message)


class DatasetNotFoundException(Exception):
    """
    Exception raised when a dataset is not found.

    This exception does not require any additional attributes beyond the default message.
    """

    def __init__(self):
        """
        Initializes an instance of DatasetNotFoundException without any specific message.

        The default message "Dataset not found" is used.
        """
        super().__init__("Dataset not found")


class FileMetadataNotFoundException(Exception):
    """
    Exception raised when file metadata is not found.

    This exception is used to indicate that the metadata for a specific file is missing
    or could not be retrieved, which may impact operations that depend on that metadata.
    """

    def __init__(self):
        """
        Initializes an instance of FileMetadataNotFoundException with a default message.

        The default message "File metadata not found" is used to indicate the error.
        """
        super().__init__("File metadata not found")


class FailedReadFileException(Exception):
    """
    Exception raised when a file reading operation fails.

    This exception carries a specific error message detailing the cause of the failure.
    """

    def __init__(self, message: str):
        """
        Initializes an instance of FailedReadFileException with a specific error message.

        Args:
            message(str): The error message to be reported.
        """
        super().__init__(message)
