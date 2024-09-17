class IncorrectFileFormatException(Exception):
    """
    Exception raised when a file format is incorrect or not supported.

    :param message: The error message to be reported.
    :type message: str
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
