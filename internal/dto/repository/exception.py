class ModelNotFoundException(Exception):
    """
    Exception raised when a storage model is not found in some data storage.

    This exception may be thrown only by the repository.
    """

    def __init__(self, message: str):
        """
        Initializes an instance of ModelNotFoundException with a default message.
        """
        super().__init__(message)
